from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot.config import REDIS_CONFIG, BOT_TOKEN

bot = Bot(token=BOT_TOKEN, validate_token=True)
redis_storage = RedisStorage2(**REDIS_CONFIG)
dispatcher = Dispatcher(bot, storage=redis_storage)
