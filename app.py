import asyncio

from aiogram.utils import executor

from config import base_commands
from core import dp, logger, set_my_commands, storage
from handlers.registration_handlers import registrate_all_handlers
from tests.gen_ord import generate_random_orders
from utils.task_scheduler import task_scheduler


# noinspection PyUnusedLocal
async def on_startup_app(dispatcher=dp):
    registrate_all_handlers()
    await storage.reset_all(True)
    # await generate_random_orders(100000)
    asyncio.create_task(set_my_commands(command_list=base_commands))
    asyncio.create_task(task_scheduler())
    logger.info('app.py: on_startup_app')


async def on_shutdown_app(dispatcher=dp):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info('app.py: on_shutdown_app')


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup_app, on_shutdown=on_shutdown_app)
    except Exception as e:
        logger.error(f"__main__: Exception: {e.args}")
