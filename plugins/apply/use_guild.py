import qqbot
from qqbot.model.ws_context import WsContext
from constant import Token, Bot_name, config
from constant.words import BotDefault
from flow.reply import reply_text
from plugins.modules.guild_info import GuildInfo
from plugins.modules.owner_info import OwnerInfo
from plugins.modules.bot_info import BotInfo

bot_api = qqbot.UserAPI(Token, False)
bot = bot_api.me()


async def robot_in_guild(context: WsContext, guilds: qqbot.Guild):
    """机器人被添加或移除事件"""

    if context.event_type == "GUILD_CREATE":
        await GuildInfo.append_or_update(
            bot_id=bot.id,
            guild_id=guilds.id,
            guild_name=guilds.name,
            guild_owner=guilds.owner_id
        )
        await BotInfo.guild_count_plus(bot.id)  # 记录机器人加入频道数
        qqbot.logger.info("机器人%s被添加进频道：%s(%s)" % (Bot_name, guilds.name, guilds.id))

        channel_api = qqbot.AsyncChannelAPI(Token, False)
        channels = await channel_api.get_channels(guilds.id)

        channel_list = []

        for i in channels:
            if i.type == 0:
                channel_list.append(i.id)

        default_status: bool = config["default"]["robot-status"]
        if default_status:
            msg = "锵锵锵，你的管理小助手驾到，希望我能帮助管理员们更好的管理频道。"
            await reply_text(
                message=qqbot.Message,
                content=msg,
                channel_id=channel_list[0],
                msg_id=context.event_id)

        status = await GuildInfo.get_robot_status(bot.id, guilds.id)
        if status is None or status is True:
            msg = "锵锵锵，你的管理小助手驾到，希望我能帮助管理员们更好的管理频道。"
            await reply_text(
                message=qqbot.Message,
                content=msg,
                channel_id=channel_list[0],
                msg_id=context.event_id)

    if context.event_type == "GUILD_DELETE":
        qqbot.logger.info("机器人被移除%s频道[ID：%s]" % (guilds.name, guilds.id))
        await BotInfo.guild_count_reduce(bot.id)  # 记录机器人被删次数
        del_guild: bool = await GuildInfo.delete_one(bot.id, guilds.id)
        del_owner: bool = await OwnerInfo.delete_one(bot.id, guilds.id)
        if del_guild is True and del_owner is True:
            msg = f"小可爱{Bot_name}被{guilds.name}({guilds.id}) 的管理员踹走了"
            print(msg)


async def robot_status(message: qqbot.Message, params=None):
    """拉黑一个频道"""

    if params == "开":
        status = True
    else:
        status = False
    await GuildInfo.set_robot_status(bot.id, message.guild_id, status)
    msg = "已将该频道加入白名单" if status else "已将该频道拉入黑名单"
    await reply_text(message=message, content=msg)
