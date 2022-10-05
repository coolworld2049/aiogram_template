from datetime import datetime, timedelta

from config import USE_SCHEDULER, NOTIFY_USER_EVERY_HOURS, NOTIFY_USER_MIN
from core import logger, scheduler


async def task_scheduler():
    if USE_SCHEDULER:
        logger.info(f'task_scheduler: RUN PENDING')
        scheduler.add_job(notify_users, 'cron', hour=NOTIFY_USER_EVERY_HOURS, minute=0, replace_existing=True)
        scheduler.start()


async def notify_users():
    orders = ...
    if len(orders) > 0 and NOTIFY_USER_MIN > 0:
        for order in orders:
            delta = datetime.timestamp(datetime.now()) - order['create_time']
            if delta >= timedelta(minutes=NOTIFY_USER_MIN):
                ...
