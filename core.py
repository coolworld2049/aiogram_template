import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import REDIS_CONFIG, USE_REDIS, TIMEZONE_UTC, BOT_TOKEN, PROJECT_NAME
from logger.logger_settings import custom_logger

logger = custom_logger(PROJECT_NAME, 'INFO', 'log.log')

scheduler = AsyncIOScheduler(timezone=TIMEZONE_UTC)

bot = Bot(token=os.environ.get('BOT_TOKEN') if os.environ.get('BOT_TOKEN') else BOT_TOKEN, validate_token=True)

dispatcher = Dispatcher(bot, storage=RedisStorage2(**REDIS_CONFIG) if USE_REDIS else MemoryStorage())

