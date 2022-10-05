from contextlib import suppress

from aiogram import types
from aiogram.types import bot_command_scope, BotCommand
from aiogram.utils.exceptions import ChatNotFound

from config import base_commands, admin_commands, ADMINS
from core import logger, bot, asyncPostgresModel
from models.database.db_api import fetchall_user_ids, fetchone_user


async def set_my_commands(users_id: int = None, command_list: list[dict[str, str]] = None):
    if not users_id:
        users = set(x['user_id'] for x in await fetchall_user_ids())
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


async def appoint_admin(user_id: int, message: types.Message) -> bool:
    user = await fetchone_user(user_id)
    user_passphrase = message.text.split(' ')[-1]
    if user:
        query = '''SELECT bot.upsert_table_user($1, $2)'''
        for username, passphrase in ADMINS.items():
            if user and user['username'] == username and user_passphrase == passphrase:
                if user['is_admin'] in [False, None]:
                    await set_my_commands(users_id=user_id, command_list=admin_commands)
                await asyncPostgresModel.executeone(query, [user_id, True])
                return True
            else:
                await asyncPostgresModel.executeone(query, [user_id, False])
                return False
