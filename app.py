import aiogram
from aiogram.utils import executor

import config
from config import RATE_LIMIT, base_commands
from core import dispatcher, logger
from filters.role_filters import RoleFilter, AdminFilter
from handlers import setup_handlers
from middlewares.role import RoleMiddleware
from middlewares.throttling import ThrottlingMiddleware
from utils.bot_mgmt import set_bot_commands
from utils.scheduler import task_scheduler


async def on_startup(_dispatcher: aiogram.Dispatcher):
    setup_handlers()
    _dispatcher.middleware.setup(ThrottlingMiddleware(limit=RATE_LIMIT))
    _dispatcher.middleware.setup(RoleMiddleware(list(config.ADMIN.items())[0][0]))
    _dispatcher.filters_factory.bind(RoleFilter)
    _dispatcher.filters_factory.bind(AdminFilter)
    await set_bot_commands(command_list=base_commands)
    await task_scheduler()
    logger.info('start')


async def on_shutdown(_dispatcher: aiogram.Dispatcher):
    await _dispatcher.storage.close()
    await _dispatcher.storage.wait_closed()
    logger.info('shutdown')


if __name__ == "__main__":
    try:
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    except aiogram.exceptions as e:
        logger.warning(f"__main__: TelegramAPIError: {e.args}")
