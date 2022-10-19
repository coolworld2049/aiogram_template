from enum import Enum

from aiogram.types import bot_command_scope, BotCommand
from loguru import logger

from bot.models.database.postgresql.api import fetchall_user_ids, fetchone_user
from core import bot
from strings.locale import common_commands


class Action(Enum):
    SET = 'set'
    DELETE = 'delete'


async def _manage_commands(users: list | set, action: Action, commands: list[dict[str, str]] = None):
    if users:
        for user_id in users:
            if commands:
                scope = bot_command_scope.BotCommandScopeChat(user_id)
                set_of_common_commands = [BotCommand(x['command'], x['description']) for x in common_commands]
                modified_commands = [BotCommand(x['command'], x['description']) for x in commands]
                set_of_common_commands.extend(modified_commands)
                if action == Action.SET:
                    await bot.set_my_commands(list(set_of_common_commands), scope)
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
