import datetime
from tortoise import fields
from tortoise.models import Model


class BotInfo(Model):
    """机器人表"""
    """机器人队列"""
    id = fields.IntField(
        pk=True,
        generated=True,
        source_field="ID",
        null=False
    )
    """机器人ID"""
    bot_id = fields.CharField(
        max_length=20,
        source_field="Bot_ID",
        null=False
    )
    """机器人名"""
    bot_name = fields.CharField(
        max_length=10,
        source_field="机器人名",
        default=""
    )
    """累计使用频道数"""
    guild_total = fields.IntField(
        max_length=5,
        source_field="累计频道数",
        default=0
    )
    """当前使用频道数"""
    guild_count = fields.IntField(
        max_length=5,
        source_field="频道数",
        default=0
    )
    """当前使用频道数"""
    guild_today = fields.IntField(
        max_length=5,
        source_field="今日频道数",
        default=30
    )
    """累计使用用户数"""
    user_total = fields.IntField(
        max_length=6,
        source_field="累计用户数",
        default=0
    )
    """当前用户数"""
    user_count = fields.IntField(
        max_length=5,
        source_field="用户数",
        default=0
    )
    """今日用户数"""
    user_today = fields.IntField(
        max_length=5,
        source_field="今日用户数",
        default=20
    )
    """累计处理消息"""
    msg_total = fields.IntField(
        max_length=10,
        source_field="累计消息",
        default=0
    )
    """今日处理消息"""
    msg_today = fields.IntField(
        max_length=5,
        source_field="今日消息",
        default=10
    )
    """最后处理时间"""
    last_time = fields.CharField(
        max_length=20,
        source_field="最后时间",
        default=""
    )

    class Meta:
        table = "bot_info"
        table_description = "机器人信息表"

    @classmethod
    async def append_or_update(cls, bot_id: str, bot_name: str) -> None:
        """注册一个机器人"""
        record, _ = await cls.get_or_create(bot_id=bot_id)
        record.bot_name = bot_name
        await record.save(update_fields=["bot_name"])

    @classmethod
    async def guild_count_plus(cls, bot_id: str) -> None:
        """当前频道数和总频道数 + 1"""
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.guild_count += 1
            record.guild_total += 1
            record.guild_today += 1
            await record.save(update_fields=["guild_count", "guild_total", "guild_today"])

    @classmethod
    async def guild_count_reduce(cls, bot_id: str) -> None:
        """当前频道数 - 1"""
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.guild_count -= 1
            await record.save(update_fields=["guild_count"])

    @classmethod
    async def user_count_plus(cls, bot_id: str) -> None:
        """当前用户数和总用户数 + 1"""
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.user_count += 1
            record.user_total += 1
            record.user_today += 1
            await record.save(update_fields=["user_count", "user_total", "user_today"])

    @classmethod
    async def user_count_reduce(cls, bot_id: str) -> None:
        """当前用户数 - 1"""
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.user_count -= 1
            await record.save(update_fields=["user_count"])

    @classmethod
    async def msg_count_plus(cls, bot_id: str) -> None:
        """今日消息数和总消息数 + 1"""
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.msg_today += 1
            record.msg_total += 1
            record.last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await record.save(update_fields=["msg_today", "msg_total", "last_time"])

    @classmethod
    async def refresh_today(cls, bot_id: str) -> None:
        """刷新今日数据"""
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.msg_today = 0
            record.guild_today = 0
            record.user_today = 0
            await record.save(update_fields=["msg_today", "guild_today", "user_today"])

    @classmethod
    async def get_bot_all(cls, bot_id: str) -> dict:
        """获取机器人所有数据"""
        record_list = await cls.filter(bot_id=bot_id)
        data = {}
        for record in record_list:
            data = {
                "guild_count": record.guild_count,
                "guild_total": record.guild_total,
                "guild_today": record.guild_today,
                "user_count": record.user_count,
                "user_total": record.user_total,
                "user_today": record.user_today,
                "msg_today": record.msg_today,
                "msg_total": record.msg_total,
                "last_time": record.last_time
            }
        return data
