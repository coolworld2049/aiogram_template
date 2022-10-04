from aiogram import types
from aiogram.types import bot_command_scope
from aiogram.utils.exceptions import ChatNotFound

from config import base_commands, admin_commands
from core import logger, bot
from data.database.db_api import is_admin, fetchall_user


async def set_my_commands(users_id: int = None, command: str = None, description: str = None,
                          command_list: list[dict[str, str]] = None):
    if not users_id:
        users = await fetchall_user()
    else:
        users = [users_id]
    if users:
        for us in users:
            list_of_base_commands = [types.BotCommand(x['command'], x['description']) for x in base_commands]
            scope = bot_command_scope.BotCommandScopeChat(chat_id=str(us))
            try:
                _current_commands = await bot.get_my_commands(scope=scope)
                current_commands = [x['command'] for x in _current_commands]
            except ChatNotFound:
                current_commands = None
            if command and description:
                list_of_base_commands.append(types.BotCommand(command, description))
                await bot.set_my_commands(list_of_base_commands, scope=scope)
            if command_list and current_commands:
                is_adm = await is_admin(us)
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
        logger.info('set_my_commands: users list EMPTY')
