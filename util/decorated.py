import qqbot
from functools import wraps
from constant import config, Token
from constant.words import BotReply
from flow.reply import reply_text

ROLE_MANAGER = "2"
ROLE_CREATOR = "4"
ROLE_CHANNEL = "5"
ROLE_HEIMU = ""  # 拥有权限的身份组ID
NAME_MANAGER = "管理员"
NAME_ALL = "全体管理"
NAME_HEIMU = "黑幕人员"
NAME_CHANNEL = "子频道管理"
NAME_SUPEROWNER = "超级管理员"


class Command:
    """指令命名"""

    def __init__(self, command):
        self.command = command

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            message: qqbot.Message = kwargs["message"]
            if self.command in message.content:
                qqbot.logger.debug("command %s match" % self.command)
                # 分隔指令后面的指令参数
                params = message.content.split(self.command)[1].lstrip()
                return await func(message=message, params=params)
            else:
                qqbot.logger.debug("command %s not match, skip!" % self.command)
                return False

        return decorated


class Role:
    """指令使用角色"""

    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        async def authority_crete(message):
            """频道主判断"""
            member_api = qqbot.AsyncGuildMemberAPI(Token, False)
            member = await member_api.get_guild_member(message.guild_id, message.author.id)
            if ROLE_CREATOR in member.roles:
                return True
            else:
                return False

        async def authority_manager(message):
            # 管理员判断
            member_api = qqbot.AsyncGuildMemberAPI(Token, False)
            member = await member_api.get_guild_member(message.guild_id, message.author.id)
            if ROLE_MANAGER in member.roles or ROLE_CREATOR in member.roles:
                return True
            else:
                return False

        async def authority_channel_manager(message):
            # 子频道管理判断
            member_api = qqbot.AsyncGuildMemberAPI(Token, False)
            member = await member_api.get_guild_member(message.guild_id, message.author.id)
            if ROLE_CHANNEL in member.roles:
                return True
            else:
                return False

        async def authority_duty_owner(message):
            # 额外指定的有权限的人员
            owner = "1198230457609294660"
            if owner == message.author.id:
                return True
            return False

        @wraps(func)
        async def decorated(*args, **kwargs):
            message: qqbot.Message = kwargs["message"]
            if NAME_MANAGER in self.role and await authority_manager(message):
                return await func(*args, **kwargs)
            if NAME_HEIMU in self.role and (await authority_duty_owner(message) or await authority_manager(message)):
                return await func(*args, **kwargs)
            if NAME_CHANNEL in self.role and await authority_channel_manager(message):
                return await func(*args, **kwargs)
            if NAME_ALL in self.role and (await authority_channel_manager(message) or await authority_manager(message)):
                return await func(*args, **kwargs)
            if NAME_SUPEROWNER in self.role and (await authority_duty_owner(message) or await authority_crete(message)):
                return await func(*args, **kwargs)
            await reply_text(message, BotReply.NO_AUTHORITY)
            return True

        return decorated
