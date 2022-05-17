import qqbot
from tortoise import Tortoise


async def database_init():
    """
    初始化建表
    """
    qqbot.logger.debug('正在注册数据库')
    database_path = "resource/data/data.db"
    db_url = f'sqlite://{database_path}'
    # 这里填要加载的表
    models = [
        'plugins.modules.guild_info',
        'plugins.modules.owner_info',
        'plugins.modules.bot_info'
    ]
    modules = {"models": models}
    await Tortoise.init(db_url=db_url, modules=modules)
    await Tortoise.generate_schemas()  # 注册表时取消注释
    qqbot.logger.debug('数据库注册完成')

# if __name__ == "__main__":
#     run_async(database_init())
