import asyncio

import aiogram
from aiogram.utils import executor

from config import base_commands
from core import dp, logger
from handlers.registration_handlers import setup_handlers
from utils.bot_mgmt import set_my_commands
from utils.scheduler import task_scheduler


# noinspection PyUnusedLocal
async def on_startup_app(dispatcher: aiogram.Dispatcher):
    setup_handlers()
    asyncio.create_task(set_my_commands(command_list=base_commands))
    asyncio.create_task(task_scheduler())
    logger.info('app.py: start')


async def on_shutdown_app(dispatcher: aiogram.Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info('app.py: shutdown')


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup_app, on_shutdown=on_shutdown_app)
    except Exception as e:
        logger.warning(f"__main__: Exception: {e.args}")
