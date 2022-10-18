from datetime import datetime, timedelta

from bot.config import USE_SCHEDULER, NOTIFY_USER_EVERY_HOURS, NOTIFY_USER_DELTA_MIN
from core import scheduler
from loguru import logger


async def bot_scheduler():
    if USE_SCHEDULER:
        logger.info(f'task_scheduler: RUN PENDING')
        scheduler.add_job(notify_users, 'cron', hour=NOTIFY_USER_EVERY_HOURS, minute=0)
        scheduler.start()


async def notify_users():
    orders = ...
    if len(orders) > 0 and NOTIFY_USER_DELTA_MIN > 0:
        for order in orders:
            delta = datetime.timestamp(datetime.now()) - order['create_time']
            if delta >= timedelta(minutes=NOTIFY_USER_DELTA_MIN):
                ...
