from tortoise import fields
from tortoise.models import Model
from typing import Optional, List


class GuildInfo(Model):
    """频道管理表"""
    """频道事件队列"""
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
    """频道ID"""
    guild_id = fields.CharField(
        max_length=20,
        source_field="频道ID",
        null=False
    )
    """频道名"""
    guild_name = fields.CharField(
        max_length=20, 
        source_field="频道名",
        default=False
        )
    """频道创建者ID"""
    guild_owner = fields.CharField(
        max_length=20,
        source_field="频道主ID",
        default=False
    )
    """机器人状态"""
    robot_status = fields.BooleanField(
        source_field="机器人状态",
        default=True)
    """转发子频道"""
    forward_channel = fields.CharField(
        max_length=20,
        source_field="转发子频道",
        default=""
    )

    class Meta:
        table = "guild_info"
        table_description = "频道信息表"

    @classmethod
    async def get_guild_list(cls, bot_id: str) -> List[str]:
        """返回开启机器人的频道列表"""
        record = await cls.filter(bot_id=bot_id)
        guild_list = []
        for one in record:
            if one.robot_status:
                guild_list.append(one.guild_id)
        return guild_list

    @classmethod
    async def get_guild_name(cls, bot_id: str, guild_id: str) -> Optional[str]:
        """获取频道名称"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        return None if record is None else record.guild_name

    @classmethod
    async def set_forward_channel(cls, bot_id: str, guild_id: str, channel_id: str) -> bool:
        """设置转发子频道"""
        record: GuildInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        if record is not None:
            record.forward_channel = channel_id
            await record.save(update_fields=["forward_channel"])
            return True
        else:
            return False

    @classmethod
    async def get_forward_channel(cls, bot_id: str, guild_id: str) -> Optional[str]:
        """获取转发子频道"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        return None if record is None else record.forward_channel

    @classmethod
    async def get_robot_status(cls, bot_id: str, guild_id: str) -> Optional[bool]:
        """获取机器人在某个频道拉黑没"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        return None if record is None else record.robot_status

    @classmethod
    async def set_robot_status(cls, bot_id: str, guild_id: str, status: bool) -> bool:
        """设置机器人开关状态"""
        record: GuildInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        if record is not None:
            record.robot_status = status
            await record.save(update_fields=["robot_status"])
            return True
        else:
            return False

    @classmethod
    async def check_guild_init(cls, bot_id: str, guild_id: str) -> bool:
        """检查频道是否已注册"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        return record is not None

    @classmethod
    async def append_or_update(cls, bot_id: str, guild_id: str, guild_name: str, guild_owner: str) -> None:
        """更新或增加一个频道信息"""
        record, _ = await cls.get_or_create(bot_id=bot_id, guild_id=guild_id)
        record.guild_name = guild_name
        record.guild_owner = guild_owner
        await record.save(update_fields=["guild_name", "guild_owner"])

    @classmethod
    async def get_all_data(cls, bot_id: str) -> List[dict]:
        """获取所有频道数据 返回 列表套字典"""
        record_list = await cls.filter(bot_id=bot_id)
        data = []
        for record in record_list:
            one_data = {'guild_id': record.guild_id,
                        'guild_name': record.guild_name,
                        'guild_owner': record.guild_owner,
                        'robot_status': record.robot_status}
            data.append(one_data)
        return data

    @classmethod
    async def change_status_all(cls, bot_id: str, status: bool) -> None:
        """改变机器人在所有频道的开关"""
        await cls.filter(bot_id=bot_id).update(robot_status=status)

    @classmethod
    async def delete_one(cls, bot_id: str, guild_id: str) -> bool:
        """删除一个频道的全部数据"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        if record is not None:
            await record.delete()
            return True
        return False

    @classmethod
    async def delete_bot(cls, bot_id: str) -> None:
        """删除一个机器人的数据"""
        await cls.filter(bot_id=bot_id).delete()
