import qqbot

from constant import Token
from plugins.modules.bot_info import BotInfo
from flow.reply import reply_text

bot_api = qqbot.UserAPI(Token, False)
bot = bot_api.me()


async def bot_totals(message: qqbot.Message):
    """查看机器人详细数据"""
    data: dict = await BotInfo.get_bot_all(bot.id)
    msg = f"""￣￣￣￣￣￣＼数据统计／￣￣￣￣￣￣
1️⃣当前加入频道：{data["guild_count"]}个
2️⃣当前使用用户：{data["user_count"]}人
3️⃣当前处理消息：{data["msg_today"]}条
————————————————
4️⃣累计加入频道：{data["guild_total"]}个
5️⃣累计使用用户：{data["user_total"]}人
6️⃣累计处理消息：{data["msg_total"]}条
*️⃣最后处理时间：{data["last_time"]}
"""
    await reply_text(
        message=message,
        content=msg
    )
