from aiogram import types

from bot.strings.answer_blanks import help_TEXT
from core import dispatcher
from bot.filters.command_filters import command_help
from bot.utils.chat_mgmt import delete_previous_messages, save_message


def reg_help_handler():
    dispatcher.register_message_handler(help_command, command_help)


@dispatcher.message_handler(command_help)
async def help_command(message: types.Message):
    await delete_previous_messages(tgtype=message)
    msg = await message.answer(help_TEXT)
    await save_message(message.from_user.id, msg.message_id)
