from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import REDIS_CONFIG, BOT_TOKEN, USE_REDIS

bot = Bot(token=BOT_TOKEN, validate_token=True)
redis_storage = RedisStorage2(**REDIS_CONFIG) if USE_REDIS else MemoryStorage()
dispatcher = Dispatcher(bot, storage=redis_storage)
