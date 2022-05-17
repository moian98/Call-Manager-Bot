import qqbot
import asyncio
import time
from constant import Token
from qqbot.model.ws_context import WsContext
from constant.words import BotReply
from flow.reply import reply_text
from util.decorated import Command, Role
from util.database import database_init
from plugins.apply.use_guild import (
    robot_status,
    robot_in_guild,
    forward_channel,
    problem_feedback
)
from plugins.apply.use_owner import (
    owner_init,
    owner_channel,
    delete_channel,
    owner_sign_in,
    owner_sign_out,
    get_sign_user,
    get_sign_ol,
    delete_owner,
    direct_status,
    see_me
)
from plugins.apply.use_bot import bot_totals
from plugins.modules.guild_info import GuildInfo
from plugins.modules.bot_info import BotInfo
from flow.scheduler import start_schedule_processes

bot_api = qqbot.UserAPI(Token, False)
bot = bot_api.me()


@Command("帮助")
async def handle_get_help(message: qqbot.Message, params=None):
    """帮助指令"""
    await reply_text(message, content=BotReply.DUTY_HELP)
    return True


@Command("菜单")
async def handle_get_menu(message: qqbot.Message, params=None):
    """帮助指令"""
    await reply_text(message, content=BotReply.DUTY_HELP)
    return True


@Command("管理注册")
@Role("全体管理")
async def handler_owner_init(message: qqbot.Message, params=None):
    await owner_init(message)
    return True


@Command("添加子频道")
@Role("子频道管理")
async def handler_owner_channel(message: qqbot.Message, params=None):
    await owner_channel(message)
    return True


@Command("删除子频道")
@Role("子频道管理")
async def handler_delete_channel(message: qqbot.Message, params=None):
    await delete_channel(message)
    return True


@Command("管理签到")
async def handler_owner_sign_in(message: qqbot.Message, params=None):
    await owner_sign_in(message)
    return True


@Command("管理签退")
async def handler_owner_sign_out(message: qqbot.Message, params=None):
    await owner_sign_out(message)
    return True


@Command("召唤管理")
async def handler_get_owner(message: qqbot.Message, params=None):
    await get_sign_user(message)
    return True


@Command("查看在线管理")
async def handler_get_owner_ol(message: qqbot.Message, params=None):
    await get_sign_ol(message)
    return True


@Command("私信通知")
async def handler_direct_open(message: qqbot.Message, params=None):
    if params is None or params == "":
        return False
    await direct_status(message, params)
    return True


@Command("查看信息")
async def handler_see_me(message: qqbot.Message, params=None):
    await see_me(message, params)
    return True


@Command("设置反馈子频道")
@Role("管理员")
async def handler_forward_channel(message: qqbot.Message, params=None):
    await forward_channel(message)
    return True


@Command("反馈问题")
async def handler_problem_feedback(message: qqbot.Message, params=None):
    if params is None or params == "":
        return False
    await problem_feedback(message, params)
    return True


@Command("问题反馈")
async def handler_problem_feedback_1(message: qqbot.Message, params=None):
    if params is None or params == "":
        return False
    await problem_feedback(message, params)
    return True


@Command("删除管理")
@Role("超级管理员")
async def handler_delete_owner(message: qqbot.Message, params=None):
    if params is None or params == "":
        return False
    await delete_owner(message)
    return True


@Command("查看统计")
@Role("超级管理员")
async def handler_see_totals(message: qqbot.Message, params=None):
    await bot_totals(message)
    return True


async def _at_message_handler(event, message: qqbot.Message):
    """注册@消息事件"""
    """频道被拉黑的话不执行"""
    bot_status: bool = await GuildInfo.get_robot_status(bot.id, message.guild_id)
    if bot_status is None or bot_status is False:
        return await reply_text(
            message=message,
            content="该频道已被拉黑，无法使用本机器人"
        )
    await BotInfo.msg_count_plus(bot_id=bot.id)  # 记录机器人处理消息数量
    guild_api = qqbot.AsyncGuildAPI(Token, False)
    guild = await guild_api.get_guild(message.guild_id)
    channel_api = qqbot.AsyncChannelAPI(Token, False)
    channel = await channel_api.get_channel(message.channel_id)
    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    member = await member_api.get_guild_member(message.guild_id, message.author.id)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    # 打印logger信息
    qqbot.logger.info(
        "[%s]收到来自频道：%s(%s) 子频道：%s(%s) 内的用户：%s(%s) 的@消息：%s" % (
            now_time,
            guild.name,
            message.guild_id,
            channel.name,
            message.channel_id,
            member.nick,
            message.author.id,
            message.content
        )
    )

    # 注册指令handler
    handlers = [
        handle_get_help,  # 帮助
        handle_get_menu,  # 菜单
        handler_owner_init,  # 管理注册
        handler_owner_channel,  # 添加子频道
        handler_delete_channel,  # 删除子频道
        handler_owner_sign_in,  # 管理签到
        handler_owner_sign_out,  # 管理签退
        handler_get_owner,  # 召唤管理
        handler_get_owner_ol,  # 查看在线管理
        handler_see_me,  # 查看信息
        handler_direct_open,  # 私信开关
        handler_forward_channel,  # 设置反馈子频道
        handler_problem_feedback,  # 问题反馈
        handler_problem_feedback_1,  # 问题反馈
        handler_delete_owner,  # 删除管理
        handler_see_totals,  # 查看统计
    ]
    for handler in handlers:
        if await handler(message=message):
            return
        # return
    await reply_text(message, BotReply.NO_MATCH_REPLY)


async def _guild_handler(context: WsContext, guild: qqbot.Guild):
    """注册频道事件"""
    await robot_in_guild(context, guild)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database_init())
    # loop.run_until_complete(BotInfo.append_or_update(bot.id, bot.username))
    # 执行定时任务
    start_schedule_processes()

    # 事件回调
    at_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _at_message_handler)
    guild_handler = qqbot.Handler(qqbot.HandlerType.GUILD_EVENT_HANDLER, _guild_handler)
    qqbot.async_listen_events(Token, False, at_handler, guild_handler)

    loop.run_forever()
