import qqbot

from constant import config

Token = qqbot.Token(config["token"]["appid"], config["token"]["token"])

ROLE_MANAGER = "2"


async def isBot(message: qqbot.Message):
    """判断机器人是否为管理员"""
    bot_api = qqbot.AsyncUserAPI(Token, False)
    bot = await bot_api.me()
    member_api = qqbot.AsyncGuildMemberAPI(Token, False)
    bot_member = await member_api.get_guild_member(message.guild_id, bot.id)
    if ROLE_MANAGER in bot_member.roles:
        return True
    else:
        return False