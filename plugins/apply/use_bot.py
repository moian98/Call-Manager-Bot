import qqbot

from constant import Token
from plugins.modules.bot_info import BotInfo
from plugins.modules.owner_info import OwnerInfo
from flow.reply import reply_text

bot_api = qqbot.UserAPI(Token, False)
bot = bot_api.me()


async def bot_totals(message: qqbot.Message):
    """查看机器人详细数据"""
    data: dict = await BotInfo.get_bot_all(bot.id)
    user_data: list = await OwnerInfo.get_bot_all(bot.id)
    user_count = len(user_data)
    msg = f"""￣￣￣￣￣￣＼数据统计／￣￣￣￣￣￣
1️⃣今日新增频道：{data["guild_today"]}个
2️⃣今日新增用户：{data["user_today"]}人
3️⃣今日处理消息：{data["msg_today"]}条
—————————————
4️⃣当前加入频道：{data["guild_count"]}个
5️⃣当前使用用户：{user_count}人
—————————————
6️⃣累计加入频道：{data["guild_total"]}个
7️⃣累计使用用户：{data["user_total"]}人
8️⃣累计处理消息：{data["msg_total"]}条
*️⃣最后处理时间：{data["last_time"]}
"""
    await reply_text(
        message=message,
        content=msg
    )
