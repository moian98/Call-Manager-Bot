import asyncio

import qqbot
import schedule
import time
from multiprocessing import Process
from plugins.modules.bot_info import BotInfo
from constant.words import BotDefault
from util.database import database_init


def start_schedule_processes():
    p = Process(target=schedule_sign_notify)
    p.start()


def schedule_sign_notify():
    """
    每天定时提醒签到
    """

    schedule.every().day.at("01:30").do(refresh_bot_today)

    while True:
        schedule.run_pending()
        time.sleep(1)


def refresh_bot_today():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(database_init())
        loop.run_until_complete(
            BotInfo.refresh_today(BotDefault.DEFAULT_BOT)
        )
        qqbot.logger.info("定时刷新已执行！")
    except Exception as e:
        qqbot.logger.info("错误: %s" % e)