import asyncio

import aiogram
import nest_asyncio
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from bot import config
from bot.config import RATE_LIMIT, common_commands
from bot.filters.role_filters import RoleFilter, AdminFilter
from bot.handlers import setup_handlers
from bot.middlewares.role import RoleMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.utils.bot_mgmt import set_bot_commands
from bot.utils.scheduler import bot_scheduler
from core import dispatcher
from services.journal.logger import logger
from services.server_statistics import setup_server_stats_handlers
from services.server_statistics.main import server_stats_run

nest_asyncio.apply()
loop = asyncio.get_event_loop()


async def on_startup(_):
    setup_server_stats_handlers()
    setup_handlers()
    dispatcher.middleware.setup(ThrottlingMiddleware(limit=RATE_LIMIT))
    dispatcher.middleware.setup(LoggingMiddleware(logger))
    dispatcher.middleware.setup(RoleMiddleware(config.ADMINS, config.MANAGERS))
    dispatcher.filters_factory.bind(RoleFilter)
    dispatcher.filters_factory.bind(AdminFilter)
    loop.run_until_complete(set_bot_commands(command_list=common_commands))
    loop.run_until_complete(bot_scheduler())
    logger.info('start')


async def on_shutdown(_):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info('shutdown')


if __name__ == "__main__":
    try:
        loop.create_task(server_stats_run())
    except Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: server_stats_service: Exception: {e.args}")

    try:
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    except aiogram.exceptions and Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: bot: TelegramAPIError: {e.args}")
