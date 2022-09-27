from aiogram import types

from core import dp


def reg_help_handler():
    dp.register_message_handler(help_command, commands=['help'])


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer('...')
