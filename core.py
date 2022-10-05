import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.storage import RATE_LIMIT
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import REDIS_CONFIG, USE_REDIS, PG_DSN, timezone
from models.database.model import AsyncPostgresModel
from utils.logger_settings import custom_logger
from utils.throttling import ThrottlingMiddleware

# ---Logging
logger = custom_logger('global_logger', logging.INFO)

# ---Bot
bot = Bot(token=os.environ["BOT_TOKEN"], validate_token=True)
if USE_REDIS:
    storage = RedisStorage2(**REDIS_CONFIG)
else:
    storage = MemoryStorage()

# ---Dispatcher
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware(limit=RATE_LIMIT))
dp.middleware.setup(LoggingMiddleware(logger))

# ---Database
asyncPostgresModel = AsyncPostgresModel(PG_DSN)

# ---Scheduler
scheduler = AsyncIOScheduler(timezone=timezone)
