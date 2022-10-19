import asyncio
import logging

import aiogram
import nest_asyncio
from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loguru import logger

from bot import config
from bot.config import RATE_LIMIT
from bot.filters.role_filters import RoleFilter, AdminFilter
from bot.handlers import setup_handlers
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.services.server_statistics import setup_server_statistics_handlers
from bot.utils.command_mgmt import manage_commands, Action
from core import dispatcher, redis_storage, runner
from services.healthcheck import check_redis, run_healthchek
from services.scheduler import set_scheduled_tasks, scheduler
from services.server_statistics.main import SERVICE_server_stats
from strings.locale import common_commands
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
    dispatcher.filters_factory.bind(RoleFilter)
    dispatcher.filters_factory.bind(AdminFilter)
    loop.run_until_complete(manage_commands(action=Action.SET, command_list=common_commands))
    setup_server_statistics_handlers()
    await run_healthchek()


async def on_shutdown(_):
    scheduler.shutdown()
    loop.run_until_complete(redis_storage.close())
    loop.run_until_complete(redis_storage.wait_closed())


async def on_startup_webhook(dp: Dispatcher):
    await on_startup(dp)
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)


async def on_shutdown_webhook(dp: Dispatcher):
    await on_shutdown(dp)
    await dp.bot.delete_webhook()
    logger.info("Delete Web-Hook URL: {url}", url=config.WEBHOOK_URL)


if __name__ == "__main__":
    try:
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    except aiogram.exceptions and Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: bot: TelegramAPIError: {e.args}")
    try:
        loop.create_task(SERVICE_server_stats())
    except Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: server_stats_service: Exception: {e.args}")
