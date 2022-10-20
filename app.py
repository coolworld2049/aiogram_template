import asyncio
import logging

import aiogram
import nest_asyncio
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loguru import logger

from bot import config
from bot.config import RATE_LIMIT, START_POLLING
from bot.handlers import setup_handlers
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.services.server_statistics import setup_server_statistics_handlers
from bot.utils.command_mgmt import manage_commands, ItemAction
from core import dispatcher, redis_storage
from services.healthcheck import run_healthcheck
from services.scheduler import set_scheduled_tasks, scheduler
from services.server_statistics.main import SERVICE_server_stats
from strings.commands import common_commands
from utils.logger import setup_logger

nest_asyncio.apply()
loop = asyncio.get_event_loop()


async def on_startup(_):
    setup_logger()
    setup_handlers()
    scheduler.start()
    set_scheduled_tasks()
    dispatcher.middleware.setup(LoggingMiddleware(logging.getLogger()))
    dispatcher.middleware.setup(ThrottlingMiddleware(limit=RATE_LIMIT))
    loop.run_until_complete(manage_commands(action=ItemAction.SET, command_list=common_commands))
    setup_server_statistics_handlers()
    loop.run_until_complete(run_healthcheck())


async def on_shutdown(_):
    scheduler.remove_all_jobs()
    scheduler.shutdown(wait=False)
    await redis_storage.close()
    await redis_storage.wait_closed()


async def on_startup_webhook(_):
    await on_startup(_)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)


async def on_shutdown_webhook(_):
    await on_shutdown(_)
    await dispatcher.bot.delete_webhook()
    logger.info("Delete Web-Hook URL: {url}", url=config.WEBHOOK_URL)


if __name__ == "__main__":
    try:
        EXECUTOR_CONFIG = {
            'dispatcher': dispatcher,
            'on_startup': on_startup,
            'on_shutdown': on_shutdown,
            'skip_updates': True,
        }
        if START_POLLING:
            executor.start_polling(**EXECUTOR_CONFIG)
        else:
            executor.start_webhook(**EXECUTOR_CONFIG, webhook_path=config.WEBHOOK_PATH)
    except aiogram.exceptions and Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: bot: TelegramAPIError: {e.args}")
    try:
        loop.create_task(SERVICE_server_stats())
    except Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: server_stats_service: Exception: {e.args}")
