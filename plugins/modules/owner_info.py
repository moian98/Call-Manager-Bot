import datetime
from tortoise import fields
from tortoise.models import Model
from typing import Optional, List, Union


class OwnerInfo(Model):
    """管理员表"""
    id = fields.IntField(
        pk=True,
        generated=True,
        source_field="ID",
        null=False
    )
    bot_id = fields.CharField(
        max_length=20,
        source_field="BotID",
        null=False
    )
    """"机器人ID"""
    guild_id = fields.CharField(
        max_length=20,
        source_field="频道ID",
        null=False
    )
    """频道ID"""
    user_id = fields.CharField(
        max_length=20,
        source_field="管理员ID",
        null=False
    )
    """管理员ID"""
    user_name = fields.CharField(
        max_length=30,
        source_field="管理员昵称",
        default=""
    )
    """管理员昵称"""
    user_role = fields.CharField(
        max_length=2,
        source_field="管理员权限",
        default=""
    )
    """管理员权限"""
    channels = fields.JSONField(
        source_field="管理子频道",
        default=[]
    )
    """管理子频道"""
    sign_ol = fields.BooleanField(
        source_field="是否在线",
        default=False
    )
    """是否在线"""
    sign_on_time = fields.CharField(
        max_length=20,
        source_field="签到时间",
        default=""
    )
    """签到时间"""
    sign_out_time = fields.CharField(
        max_length=20,
        source_field="签退时间",
        default=""
    )
    """签退时间"""
    duty_times = fields.IntField(
        max_length=10,
        source_field="累计时间",
        default=0
    )
    """累计值班时间"""
    duty_count = fields.IntField(
        max_length=5,
        source_field="值班次数",
        default=0
    )
    """值班次数"""
    direct_status = fields.BooleanField(
        source_field="私信开关",
        default=True
    )
    """私信开关"""

    class Meta:
        table = "owner_info"
        table_description = "管理员信息表"

    @classmethod
    async def judge_user(cls, bot_id: str, guild_id: str, user_id: str) -> bool:
        """判断管理员是否已注册"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is None:
            return False
        else:
            return True

    @classmethod
    async def get_user_name(cls, bot_id: str, guild_id: str, user_id: str) -> Optional[str]:
        """获取管理员昵称"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        return None if record is None else record.user_name

    @classmethod
    async def get_channels(cls, bot_id: str, guild_id: str, user_id: str) -> List[str]:
        """获取管理员所管理的子频道列表"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        return None if record is None else record.channels

    @classmethod
    async def get_sign_ol(cls, bot_id: str, guild_id: str, user_id: str) -> Optional[bool]:
        """获取管理员在线状态"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        return None if record is None else record.sign_ol

    @classmethod
    async def get_user_role(cls, bot_id: str, guild_id: str, user_id: str) -> Optional[str]:
        """获取管理员权限"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        return None if record is None else record.user_role

    @classmethod
    async def set_user_role(cls, bot_id: str, guild_id: str, user_id: str, user_role: str) -> bool:
        """设置管理员权限"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is not None:
            record.user_role = user_role
            await record.save(update_fields=["user_role"])
            return True
        else:
            return False

    @classmethod
    async def set_sign_in(cls, bot_id: str, guild_id: str, user_id: str) -> int:
        """管理员签到"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record.sign_ol is None:
            return 0
        if record.sign_ol is False:
            record.sign_ol = True
            record.sign_on_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await record.save(update_fields=["sign_ol", "sign_on_time"])
            return 1
        else:
            return 2

    @classmethod
    async def set_sign_out(cls, bot_id: str, guild_id: str, user_id: str) -> Union[int, bool]:
        """管理员签退"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record.sign_ol is True:
            record.sign_ol = False
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record.sign_out_time = now_time
            record.duty_count += 1
            # 计算值班时间
            sign_on = datetime.datetime.strptime(str(record.sign_on_time), "%Y-%m-%d %H:%M:%S")
            now_time_s = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
            duty_time = now_time_s - sign_on
            secs = duty_time.total_seconds()
            minute = int(secs // 60)
            record.duty_times += minute
            await record.save(update_fields=["sign_ol", "sign_out_time", "duty_count", "duty_times"])
            return minute
        else:
            return False

    @classmethod
    async def get_guild_sign(cls, bot_id: str, guild_id: str, sign_ol: bool = True) -> List[dict]:
        """获取在线管理员"""
        record_list = await cls.filter(bot_id=bot_id, guild_id=guild_id, sign_ol=sign_ol)
        data = []
        for record in record_list:
            one_data = {
                "user_id": record.user_id,
                "user_name": record.user_name,
                "channels": record.channels,
                "user_role": record.user_role
            }
            data.append(one_data)
        return data

    @classmethod
    async def set_channels(cls, bot_id: str, guild_id: str, user_id: str, channel_id: str) -> bool:
        """设置管理员所在的子频道"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is not None:
            record.channels.append(channel_id)
            await record.save(update_fields=["channels"])
            return True
        else:
            return False

    @classmethod
    async def delete_channels(cls, bot_id: str, guild_id: str, user_id: str, channel_id: str) -> bool:
        """删除一个子频道"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is not None:
            record.channels.remove(channel_id)
            await record.save(update_fields=["channels"])
            return True
        else:
            return False

    @classmethod
    async def set_direct_status(cls, bot_id: str, guild_id: str, user_id: str, status: bool) -> bool:
        """私信开关"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is not None:
            record.direct_status = status
            await record.save(update_fields=["direct_status"])
            return True
        else:
            return False

    @classmethod
    async def get_direct_status(cls, bot_id: str, guild_id: str, user_id: str) -> Optional[bool]:
        """获取管理员私信开关状态"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        return None if record is None else record.direct_status

    @classmethod
    async def add_or_update(
            cls,
            bot_id: str,
            guild_id: str,
            user_id: str,
            user_name: str,
            user_role: str
    ) -> None:
        """添加或更新一个管理员信息"""
        record, _ = await cls.get_or_create(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        record.user_name = user_name
        record.user_role = user_role
        await record.save(update_fields=["user_name", "user_role"])

    @classmethod
    async def get_user_all(cls, bot_id: str, guild_id: str, user_id: str) -> dict:
        """获取一个管理员全部数据"""
        record_list = await cls.filter(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        one_data = {}
        for record in record_list:
            one_data = {
                "user_id": record.user_id,
                "user_name": record.user_name,
                "channels": record.channels,
                "user_role": record.user_role,
                "sign_ol": record.sign_ol,
                "sign_on_time": record.sign_on_time,
                "sign_out_time": record.sign_out_time,
                "duty_times": record.duty_times,
                "duty_count": record.duty_count
            }
        return one_data

    @classmethod
    async def get_guild_all(cls, bot_id: str, guild_id: str) -> list:
        """获取一个频道全部数据"""
        record_list = await cls.filter(bot_id=bot_id, guild_id=guild_id)
        data = []
        for record in record_list:
            one_data = {
                "user_id": record.user_id,
                "user_name": record.user_name,
                "channels": record.channels,
                "user_role": record.user_role,
                "sign_ol": record.sign_ol,
                "sign_on_time": record.sign_on_time,
                "sign_out_time": record.sign_out_time,
                "duty_times": record.duty_times,
                "duty_count": record.duty_count
            }
            data.append(one_data)
        return data

    @classmethod
    async def delete_user(cls, bot_id: str, guild_id: str, user_id: str) -> bool:
        """删除一个管理员"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is not None:
            await record.delete()
            return True
        return False

    @classmethod
    async def delete_one(cls, bot_id: str, guild_id: str) -> bool:
        """删除一个频道的全部数据"""
        record = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id)
        if record is not None:
            await record.delete()
            return True
        return False

    @classmethod
    async def check_role(cls, bot_id: str, guild_id: str, user_id: str, user_name: str, role_id: str) -> None:
        """更新管理资料"""
        record: OwnerInfo = await cls.get_or_none(bot_id=bot_id, guild_id=guild_id, user_id=user_id)
        if record is not None:
            record.user_name = user_name
            record.user_role = role_id
            await record.save(update_fields=["user_name", "user_role"])
