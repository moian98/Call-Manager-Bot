import qqbot
import random
from constant import Token
from flow.reply import reply_text, reply_direct_text
from plugins.modules.owner_info import OwnerInfo
from plugins.modules.bot_info import BotInfo
from qqbot.core.exception.error import AuthenticationFailedError

bot_api = qqbot.UserAPI(Token, False)
bot = bot_api.me()

C_ROLE_ID = "5"
OW_ROLE_ID = "2"
CRETE_ROLE_ID = "4"


async def owner_init(message: qqbot.Message):
    """注册一个管理员"""
    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    member = await member_api.get_guild_member(message.guild_id, message.author.id)
    if CRETE_ROLE_ID in member.roles:
        role_id = "4"
    elif OW_ROLE_ID in member.roles:
        role_id = "2"
    elif C_ROLE_ID in member.roles:
        role_id = "5"
    else:
        return reply_text(
            message=message,
            content="❎<@%s>你不是管理员，无法注册" % message.author.id
        )
    get_user_init = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if get_user_init is True:
        await reply_text(
            message=message,
            content="❎<@%s>你已经注册过了,请勿重复注册" % message.author.id
        )
    else:
        await OwnerInfo.add_or_update(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=message.author.id,
            user_name=message.author.username,
            user_role=role_id)
        await reply_text(
            message=message,
            content="✅<@%s>管理员注册成功，请有空管理时使用指令签到，无空时请使用指令签退。\n🔵子频道管理员需先前往自己管理的子频道使用指令：@召唤管理 /添加子频道 ，来设置你所管理的子频道" % message.author.id
        )
        await BotInfo.user_count_plus(bot.id)  # 记录机器人新增用户数


async def owner_channel(message: qqbot.Message):
    """添加一个子频道"""
    judge = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if judge is False:
        return await reply_text(
            message=message,
            content="❎<@%s>你还没有注册呢，请先使用指令：@召唤管理 /管理注册" % message.author.id
        )
    channel_api = qqbot.AsyncChannelPermissionsAPI(Token, False)
    try:
        channel = await channel_api.get_channel_permissions(message.channel_id, message.author.id)
    except AuthenticationFailedError:
        return await reply_text(message=message, content="❎小召要判断你是否是此子频道的管理员，但权限不足，请授权小召为管理员。")

    if int(channel.permissions) < 6:
        return await reply_text(message=message, content="❎<@%s>你不是当前子频道的管理员，无法添加" % message.author.id)

    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    member = await member_api.get_guild_member(message.guild_id, message.author.id)
    if C_ROLE_ID in member.roles:
        channel_if: bool = await OwnerInfo.set_channels(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=message.author.id,
            channel_id=message.channel_id
        )
        if channel_if is True:
            await reply_text(message=message, content="✅<@%s>已添加本子频道为你的管理子频道" % message.author.id)
        else:
            await reply_text(message=message, content="❎<@%s>添加失败，请稍后重试" % message.author.id)
    else:
        await reply_text(message=message, content="❎<@%s>你不是当前子频道的管理员，无法使用。" % message.author.id)


async def delete_channel(message: qqbot.Message):
    """删除一个子频道"""
    judge = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if judge is False:
        return await reply_text(
            message=message,
            content="❎<@%s>你还没有注册呢，请先使用指令：@召唤管理 /管理注册" % message.author.id
        )

    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    member = await member_api.get_guild_member(message.guild_id, message.author.id)
    if C_ROLE_ID in member.roles:
        channel_if: bool = await OwnerInfo.delete_channels(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=message.author.id,
            channel_id=message.channel_id
        )
        if channel_if is True:
            await reply_text(message=message, content="✅<@%s>已将本子频道从你管理的列表中删除" % message.author.id)
        else:
            await reply_text(message=message, content="❎<@%s>你没有添加本子频道，无需删除" % message.author.id)
    else:
        await reply_text(message=message, content="❎<@%s>你不是当前子频道的管理员，无法使用。" % message.author.id)


async def owner_sign_in(message: qqbot.Message):
    """进行一次签到"""
    judge = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if judge is False:
        return await reply_text(
            message=message,
            content="❎<@%s>你还没有注册呢，请先使用指令：@召唤管理 /管理注册" % message.author.id
        )
    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    member = await member_api.get_guild_member(message.guild_id, message.author.id)
    role_id = ""
    if CRETE_ROLE_ID in member.roles:
        role_id = "4"
    elif OW_ROLE_ID in member.roles:
        role_id = "2"
    elif C_ROLE_ID in member.roles:
        role_id = "5"
    user_role = await OwnerInfo.get_user_role(bot.id, message.guild_id, message.author.id)
    channels = await OwnerInfo.get_channels(bot.id, message.guild_id, message.author.id)
    if user_role == "5" and not channels:
        return await reply_text(
            message=message,
            content="❎子频道管理员请先添加你所管理的子频道。"
        )
    if user_role != role_id:
        await OwnerInfo.check_role(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=message.author.id,
            user_name=message.author.username,
            role_id=role_id
        )
    sign_on: int = await OwnerInfo.set_sign_in(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if sign_on == 1:
        await reply_text(message=message, content="✅<@%s>值班签到成功，请值班期间留意@信息和私信。" % message.author.id)
    elif sign_on == 0:
        await reply_text(message=message, content="❎<@%s>你还没有注册呢，请先使用指令：@召唤管理 /管理注册" % message.author.id)
    else:
        await reply_text(message=message, content="❎<@%s>你已经签到过了，请不要重复签到" % message.author.id)


async def owner_sign_out(message: qqbot.Message):
    """进行一次签退"""
    judge = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if judge is False:
        return await reply_text(
            message=message,
            content="❎<@%s>你还没有注册呢，请先使用指令：@召唤管理 /管理注册" % message.author.id
        )

    sign_on = await OwnerInfo.set_sign_out(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if sign_on is False:
        await reply_text(message=message, content="❎<@%s>你还没有签到呢，请先使用指令：@召唤管理 /管理签到" % message.author.id)
    else:
        await reply_text(message=message, content="✅<@%s>值班签退成功，本次共值班%s分钟，值班期间辛苦了。"
                                                  % (message.author.id, sign_on))


async def get_sign_user(message: qqbot.Message):
    """召唤在线管理"""
    guilds: list = await OwnerInfo.get_guild_sign(bot_id=bot.id, guild_id=message.guild_id, sign_ol=True)
    if guilds is None:
        return

    if len(guilds) == 0:
        return await reply_text(message=message, content="🔍当前频道还没有签到在线的管理员")

    c_channels = []
    manager_channels = []
    crete_channel = ""
    for i in range(len(guilds)):
        if message.channel_id in guilds[i]["channels"] and guilds[i]["user_role"] == "5":
            c_channels.append(guilds[i]["user_id"])
        elif guilds[i]["user_role"] == "2":
            manager_channels.append(guilds[i]["user_id"])
        elif guilds[i]["user_role"] == "4":
            crete_channel = guilds[i]["user_id"]

    guild_api = qqbot.AsyncGuildAPI(Token, False)
    guild = await guild_api.get_guild(message.guild_id)
    if len(c_channels) > 0:
        user_id = random.choice(c_channels)
        content = "🔔已向子频道管理员<@%s>发送通知，请等候……" % user_id
        await reply_text(
            message=message,
            content=content
        )
        dir_status = await OwnerInfo.get_direct_status(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=user_id
        )
        if dir_status is True:
            await reply_direct_text(
                message=message,
                content="🔔有来自频道：%s 的频友向你发送召唤请求，请前往该频道查看。" % guild.name,
                user_id=user_id
            )
    elif len(manager_channels) > 0:
        user_id = random.choice(manager_channels)
        content = "🔔当前子频道没有签到在线的蓝牌管理员，已向绿牌管理员<@%s>发送通知，请等候……" % user_id
        await reply_text(
            message=message,
            content=content
        )
        dir_status = await OwnerInfo.get_direct_status(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=user_id
        )
        if dir_status is True:
            await reply_direct_text(
                message=message,
                content="🔔有来自频道：%s 的频友向你发送召唤请求，请前往该频道查看。" % guild.name,
                user_id=user_id
            )
    elif crete_channel != "":
        content = "🔔当前没有签到在线的蓝牌管理员，已向频道主<@%s>发送通知，请等候……" % crete_channel
        await reply_text(
            message=message,
            content=content
        )
        dir_status = await OwnerInfo.get_direct_status(
            bot_id=bot.id,
            guild_id=message.guild_id,
            user_id=crete_channel
        )
        if dir_status is True:
            await reply_direct_text(
                message=message,
                content="🔔有来自频道：%s 的频友向你发送召唤请求，请前往该频道查看。" % guild.name,
                user_id=crete_channel
            )


async def get_sign_ol(message: qqbot.Message):
    """查看在线管理员"""
    guilds: list = await OwnerInfo.get_guild_sign(bot_id=bot.id, guild_id=message.guild_id, sign_ol=True)
    if guilds is None or len(guilds) == 0:
        return await reply_text(message=message, content="🔍当前频道还没有签到在线的管理员")

    c_channels = []
    manager_channels = []
    crete_channel = ""
    for i in range(len(guilds)):
        if message.channel_id in guilds[i]["channels"] and guilds[i]["user_role"] == "5":
            c_channels.append(guilds[i]["user_id"])
        elif guilds[i]["user_role"] == "2":
            manager_channels.append(guilds[i]["user_id"])
        elif guilds[i]["user_role"] == "4":
            crete_channel = guilds[i]["user_id"]

    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    msg = "📇当前在线管理员如下：\n------------------\n"
    if len(c_channels) == 0:
        msg += "🔵子频道管理员：\n    本子频道暂无"
    else:
        msg += "🔵子频道管理员："
        for i in c_channels:
            user = await member_api.get_guild_member(message.guild_id, i)
            msg += "\n    🔹%s" % user.nick
    if len(manager_channels) > 0:
        msg += "\n🟢管理员："
        for i in manager_channels:
            user = await member_api.get_guild_member(message.guild_id, i)
            msg += "\n    🔹%s" % user.nick

    if crete_channel != "":
        user = await member_api.get_guild_member(message.guild_id, crete_channel)
        msg += "\n🔴频道主：🔹%s" % user.nick

    await reply_text(message=message, content=msg)


async def direct_status(message: qqbot.Message, params=None):
    """私信开关"""
    judge = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id
    )
    if judge is False:
        return await reply_text(
            message=message,
            content="❎<@%s>你还没有注册呢，请先使用指令：@召唤管理 /管理注册" % message.author.id
        )
    if params == "开":
        status = True
    else:
        status = False
    dir_status: bool = await OwnerInfo.set_direct_status(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=message.author.id,
        status=status
    )
    msg = "✅<@%s>私信通知已开启" if status else "✅<@%s>私信通知已关闭"
    if dir_status is True:
        await reply_text(
            message=message,
            content=msg % "%s" % message.author.id
        )
    else:
        await reply_text(message=message, content="❎出错了，稍后再试。")


async def delete_owner(message: qqbot.Message):
    """删除一个管理员"""
    user = message.mentions
    if len(user) > 2:
        return await reply_text(
            message=message,
            content="❎@的人太多了，一个一个的来吧"
        )
    delete_if: bool = await OwnerInfo.delete_user(bot_id=bot.id, guild_id=message.guild_id, user_id=user[1].id)
    if delete_if is True:
        await reply_text(
            message=message,
            content="✅删除成功！"
        )
        await BotInfo.user_count_reduce(bot.id)  # 记录机器人删除一个用户
    else:
        await reply_text(
            message=message,
            content="❎要删除的管理员不存在"
        )


async def see_me(message: qqbot.Message, params=None):
    """查看管理员信息"""
    if params is None or params == "" or params == "我":
        user_id = message.author.id
    else:
        user_id = message.mentions[1].id
    users = message.mentions
    if len(users) > 2:
        return await reply_text(
            message=message,
            content="❎@的人太多了，一个一个的来吧"
        )
    judge = await OwnerInfo.judge_user(
        bot_id=bot.id,
        guild_id=message.guild_id,
        user_id=user_id
    )
    if judge is False:
        return await reply_text(
            message=message,
            content="❎<@%s>该用户还没有注册，无法查看" % message.author.id
        )
    user = await OwnerInfo.get_user_all(bot.id, message.guild_id, user_id)
    channels = user["channels"]
    channel_text = ""
    role_name = ""
    if channels:
        for i in channels:
            channel_text = f"\n    ▫<#{i}>"
    if user["user_role"] == "5":
        role_name = f"子频道管理员  {channel_text}"
    elif user["user_role"] == "2":
        role_name = "管理员"
    elif user["user_role"] == "4":
        role_name = "频道主"
    if user["sign_ol"] is True:
        online = "是"
    else:
        online = "否"

    duty_time = "{:.1f}".format(user["duty_times"] / 60)

    msg = f"<@{user_id}>的值班信息如下：" \
          f"\n------------------" \
          f"\n🔹身份组：{role_name}" \
          f"\n🔹值班时间：{duty_time} 小时" \
          f"\n🔹值班次数：{user['duty_count']} 次" \
          f"\n🔹签退时间：{user['sign_out_time']}" \
          f"\n🔹是否在线：{online}"
    await reply_text(
        message=message,
        content=msg
    )
