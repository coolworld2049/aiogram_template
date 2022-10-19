from datetime import datetime, timedelta

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from bot.config import USE_SCHEDULER, NOTIFY_USER_EVERY_HOURS, NOTIFY_USER_DELTA_MIN

DEFAULT = "default"

jobstores = {
    DEFAULT: RedisJobStore(db=config.REDIS_CONFIG.get('db'),
                           host=config.REDIS_CONFIG.get('host'),
                           port=config.REDIS_CONFIG.get('port'))
}
executors = {DEFAULT: AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}

scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                             timezone=config.TIMEZONE_UTC)


def set_scheduled_tasks():
    if USE_SCHEDULER:
        scheduler.add_job(notify_users, 'cron', hour=NOTIFY_USER_EVERY_HOURS, minute=0)


def notify_users():
    orders = ...
    if len(orders) > 0 and NOTIFY_USER_DELTA_MIN > 0:
        for order in orders:
            delta = datetime.timestamp(datetime.now()) - order['create_time']
            if delta >= timedelta(minutes=NOTIFY_USER_DELTA_MIN):
                ...
