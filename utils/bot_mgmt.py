from contextlib import suppress

from aiogram.types import bot_command_scope, BotCommand
from aiogram.utils.exceptions import ChatNotFound

from config import base_commands
from core import logger, bot
from models.database.db_api import fetchall_user_ids


async def set_my_commands(users_id: int = None, command_list: list[dict[str, str]] = None):
    if not users_id:
        res = await fetchall_user_ids()
        users = set(x['user_id'] for x in res) if res else None
    else:
        users = [users_id]
    if users:
        for us_id in users:
            list_of_base_commands: set[BotCommand] = set(BotCommand(x['command'], x['description']) for x in base_commands)
            scope = bot_command_scope.BotCommandScopeChat(chat_id=str(us_id))
            current_commands = []
            with suppress(ChatNotFound):
                _current_commands = await bot.get_my_commands(scope=scope)
                if _current_commands:
                    current_commands = [x['command'] for x in _current_commands]
            if command_list:
                for command in [BotCommand(x['command'], x['description']) for x in command_list]:
                    if command['command'] not in current_commands:
                        list_of_base_commands.add(command)
                await bot.set_my_commands(list(list_of_base_commands), scope=scope)
    else:
        logger.info('set_commands: no users')



