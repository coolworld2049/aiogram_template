from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from config import help_TEXT
from core import dp


def reg_help_handler():
    dp.register_message_handler(help_command, CommandHelp())


@dp.message_handler(CommandHelp())
async def help_command(message: types.Message):
    await message.answer(help_TEXT)
