import logging
import os
import sys

import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import bot_command_scope
from aiogram.utils.exceptions import ChatNotFound

from config import base_commands, admin_commands, PATH_TO_LOG_FILE, REDIS_CONFIG, USE_REDIS, ADMINS
from data.database.database import executeone, fetchmany
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
scheduler = aioschedule.Scheduler()


async def set_my_commands(users_id: int = None, command: str = None, description: str = None,
                          command_list: list[dict[str, str]] = None):
    if not users_id:
        users = await fetchmany('''SELECT * FROM bot.user''')
    else:
        users = [users_id]
    if len(users) > 0:
        for u_id in users:
            list_of_base_commands = [types.BotCommand(x['command'], x['description']) for x in base_commands]
            scope = bot_command_scope.BotCommandScopeChat(chat_id=str(u_id))
            try:
                _current_commands = await bot.get_my_commands(scope=scope)
                current_commands = [x['command'] for x in _current_commands]
            except ChatNotFound:
                current_commands = None
            if command and description:
                list_of_base_commands.append(types.BotCommand(command, description))
                await bot.set_my_commands(list_of_base_commands, scope=scope)
            if command_list and current_commands:
                is_adm = await is_admin(u_id)
                if not is_adm:
                    new = command_list
                else:
                    new = admin_commands
                list_of_new_commands = [types.BotCommand(x['command'], x['description']) for x in new]
                for command in list_of_new_commands:
                    if command['command'] not in current_commands:
                        list_of_base_commands.append(command)
                await bot.set_my_commands(list_of_base_commands, scope=scope)
    else:
        logger.info('set_my_commands: users_id list EMPTY')


async def is_admin(user_id: int):
    users = await fetchmany("""SELECT * FROM bot.user WHERE user_id = $1""", [user_id])
    if len(users) != 0:
        for us in users:
            query = """INSERT INTO bot.user(user_id, is_admin) VALUES ($1,$2) ON CONFLICT DO NOTHING"""
            if us['username'] in ADMINS:
                await executeone(query, [user_id, True])
                return True
            else:
                await executeone(query, [user_id, False])
                return False
