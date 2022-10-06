from aiogram import types

from lang import help_TEXT
from core import dp
from filters.command_filters import command_help
from utils.chat_mgmt import delete_previous_messages


def reg_help_handler():
    dp.register_message_handler(help_command, command_help)


@dp.message_handler(command_help)
async def help_command(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await message.answer(help_TEXT)
