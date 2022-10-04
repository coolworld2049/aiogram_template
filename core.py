import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aioschedule import Scheduler

from config import REDIS_CONFIG, USE_REDIS, USE_LOCAL_SERVER
from utils.throttling import ThrottlingMiddleware

# ---Logging
logger = logging.Logger('global_logger', logging.INFO)

# ---Bot
local_server = TelegramAPIServer.from_base('http://localhost')
bot = Bot(token=os.environ["BOT_TOKEN"], validate_token=True, server=local_server if USE_LOCAL_SERVER else None)
if USE_REDIS:
    storage = RedisStorage2(**REDIS_CONFIG)
else:
    storage = MemoryStorage()

# ---Dispatcher
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware())
dp.middleware.setup(LoggingMiddleware(logger))

# ---Scheduler
scheduler = Scheduler()



