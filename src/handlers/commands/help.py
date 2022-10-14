from aiogram import types

from answer_blanks.lang import help_TEXT
from core import dispatcher
from filters.command_filters import command_help
from utils.chat_mgmt import delete_previous_messages


def reg_help_handler():
    dispatcher.register_message_handler(help_command, command_help)


@dispatcher.message_handler(command_help)
async def help_command(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await message.answer(help_TEXT)
