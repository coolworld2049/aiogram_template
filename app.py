import asyncio
import logging

import aiogram
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loguru import logger

from bot import config
from bot.commands.commands_config import common_commands
from bot.config import RATE_LIMIT, START_POLLING, RUN_ON_DOCKER
from bot.filters.roles import RoleFilter, AdminFilter
from bot.handlers.setup import setup_handlers
from bot.middlewares.album import AlbumMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.services.healthcheck import run_healthcheck
from bot.utils.command_mgmt import manage_commands, ItemAction
from bot.utils.logger import setup_logger
from core import dispatcher, redis_storage


async def on_startup(_):
    setup_logger()
    setup_handlers()
    dispatcher.middleware.setup(LoggingMiddleware(logging.getLogger()))
    dispatcher.middleware.setup(ThrottlingMiddleware(limit=RATE_LIMIT))
    dispatcher.middleware.setup(AlbumMiddleware())
    dispatcher.filters_factory.bind(RoleFilter)
    dispatcher.filters_factory.bind(AdminFilter)
    asyncio.create_task(manage_commands(action=ItemAction.SET, command_list=common_commands))
    asyncio.create_task(run_healthcheck())


async def on_shutdown(_):
    await redis_storage.close()
    await redis_storage.wait_closed()


if __name__ == "__main__":
    try:
        logger.info(f'RUN_ON_DOCKER: {RUN_ON_DOCKER}')
        EXECUTOR_CONFIG = {
            'dispatcher': dispatcher,
            'on_startup': on_startup,
            'on_shutdown': on_shutdown,
            'skip_updates': True,
        }
        if START_POLLING:
            executor.start_polling(**EXECUTOR_CONFIG)
    except aiogram.exceptions and Exception as e:
        logger.exception(f"{config.PROJECT_NAME}: bot: TelegramAPIError: {e.args}")
