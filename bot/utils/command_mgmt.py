from contextlib import suppress
from enum import Enum

from aiogram.types import bot_command_scope, BotCommand
from aiogram.utils.exceptions import ChatNotFound
from loguru import logger

from strings.locale import common_commands
from core import bot
from bot.models.database.postgresql.api import fetchall_user_ids, fetchone_user


class Action(Enum):
    SET = 'set'
    DELETE = 'delete'


async def _manage_commands(users: list | set, action: Action, command_list: list[dict[str, str]] = None):
    if users:
        for user_id in users:
            list_of_base_commands = set(BotCommand(x['command'], x['description']) for x in common_commands)
            scope = bot_command_scope.BotCommandScopeChat(chat_id=str(user_id))
            with suppress(ChatNotFound):
                current_commands = []
                _current_commands = await bot.get_my_commands(scope=scope)
                if _current_commands:
                    current_commands = [x['command'] for x in _current_commands]
            if command_list:
                for command in [BotCommand(x['command'], x['description']) for x in command_list]:
                    if command['command'] not in current_commands:
                        list_of_base_commands.add(command)
                if action == Action.SET:
                    await bot.set_my_commands(list(list_of_base_commands), scope)
                elif action == Action.DELETE and scope:
                    await bot.delete_my_commands(scope)


async def manage_commands(action: Action, users_id: int = None, command_list: list[dict[str, str]] = None):
    if users_id:
        res = await fetchone_user(users_id)
        users = [res['user_id']] if res else logger.info(f'set_bot_commands: users_id {users_id}: no user')
    else:
        res = await fetchall_user_ids()
        users = [x['user_id'] for x in res] if res else logger.info('set_bot_commands: no users')
    await _manage_commands(users, action, command_list)
