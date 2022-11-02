import io

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import config
from bot.config import USE_SCHEDULER, NOTIFY_USER_EVERY_HOURS

DEFAULT = "default"

jobstores = {
    DEFAULT: RedisJobStore(db=config.REDIS_JOBSTORE_DB,
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
        scheduler.print_jobs(jobstore=DEFAULT, out=io.open(config.BASE_LOG_PATH, mode='a'))


def notify_users():
    print('notify_users')
