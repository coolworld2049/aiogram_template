import asyncio
from datetime import datetime, timedelta

from config import USE_SCHEDULER, NOTIFY_USER_EVERY_HOURS, NOTIFY_USER_MIN
from core import logger, scheduler


async def task_scheduler():
    if USE_SCHEDULER:
        logger.info(f'task_scheduler: RUN PENDING')
        JOBS = [
            scheduler.every(NOTIFY_USER_EVERY_HOURS).hours.do(notify_users, NOTIFY_USER_MIN)
        ]
        scheduler.jobs.clear()
        scheduler.jobs.extend(JOBS)
        jsoin_str = ",\n"
        logger.info(f'task_scheduler: current tasks:\n\n{jsoin_str.join(map(str, scheduler.jobs))}\n')
        while True:
            await scheduler.run_pending()
            await asyncio.sleep(1)


async def notify_users(custom_time: int):
    orders = ...
    if len(orders) > 0 and custom_time > 0:
        for order in orders:
            delta = datetime.timestamp(datetime.now()) - order['create_time']
            if delta >= timedelta(minutes=custom_time):
                ...
