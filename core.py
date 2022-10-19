from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor

from bot.config import REDIS_CONFIG, BOT_TOKEN

app_dir: Path = Path(__file__).parent.parent
locales_dir = app_dir / "locales"

bot = Bot(token=BOT_TOKEN, validate_token=True)
redis_storage = RedisStorage2(**REDIS_CONFIG)
dispatcher = Dispatcher(bot, storage=redis_storage)
runner = Executor(dispatcher, skip_updates=True)
