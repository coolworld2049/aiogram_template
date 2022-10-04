import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aioschedule import Scheduler

from config import REDIS_CONFIG, USE_REDIS, PATH_TO_LOG_FILE
from utils.throttling import ThrottlingMiddleware

# ---Logging
logger = logging.Logger('global_logger', logging.INFO)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, encoding="utf-8")
stream_handler = logging.StreamHandler(sys.stderr)
row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
file_handler.setFormatter(logging.Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
stream_handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# ---Bot
bot = Bot(token=os.environ["BOT_TOKEN"], validate_token=True)
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



