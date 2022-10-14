import aiogram
from aiogram.utils import executor

from bot import config
from bot.config import RATE_LIMIT, base_commands
from core import dispatcher, logger
from bot.filters.role_filters import RoleFilter, AdminFilter
from bot.handlers import setup_handlers
from bot.middlewares.role import RoleMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.utils.bot_mgmt import set_bot_commands
from bot.utils.scheduler import task_scheduler


async def on_startup(dp: aiogram.Dispatcher):
    setup_handlers()
    dp.middleware.setup(ThrottlingMiddleware(limit=RATE_LIMIT))
    dp.middleware.setup(RoleMiddleware(list(config.ADMIN.items())[0][0]))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    await set_bot_commands(command_list=base_commands)
    await task_scheduler()
    logger.info('start')


async def on_shutdown(dp: aiogram.Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('shutdown')


if __name__ == "__main__":
    try:
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    except aiogram.exceptions as e:
        logger.warning(f"{config.PROJECT_NAME}: TelegramAPIError: {e.args}")
