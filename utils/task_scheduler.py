import asyncio
from datetime import datetime

from config import USE_SCHEDULER, NOTIFY_USER_EVERY_HOURS, NOTIFY_USER
from core import logger, scheduler


async def task_scheduler():
    if USE_SCHEDULER:
        logger.info(f'task_scheduler: RUN PENDING')
        JOBS = [
            scheduler.every(NOTIFY_USER_EVERY_HOURS).hours.do(notify_users, NOTIFY_USER)
        ]
        scheduler.jobs.clear()
        scheduler.jobs.extend(JOBS)
        jsoin_str = ",\n"
        logger.info(f'task_scheduler: current tasks:\n\n{jsoin_str.join(map(str, scheduler.jobs))}\n')
        while True:
            await scheduler.run_pending()
            await asyncio.sleep(1)


async def notify_users(custom_time: int):
    """orders = await fetchmany('''SELECT * FROM bot."order" WHERE contractor_id is null AND state = $1''',
                             [OrderStates.order_accepted.state])"""
    orders = ...
    if len(orders) > 0 and custom_time > 0:
        for order in orders:
            now = datetime.timestamp(datetime.now())
            delta = now - order['create_time']
            if delta >= custom_time * 60:
                pass
