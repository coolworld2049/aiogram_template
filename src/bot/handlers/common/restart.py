import asyncio

from aiogram import types

from bot.filters.command_filters import command_restart
from bot.keyboards.user.common.common_inline_kb import base_navigation
from bot.strings.answer_blanks import restart_command_TEXT
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from core import dispatcher


def reg_restart_handlers():
    dispatcher.register_message_handler(restart, command_restart, state='*')


@dispatcher.message_handler(command_restart, state='*')
async def restart(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await dispatcher.current_state(chat=message.from_user.id, user=message.from_user.id).reset_state(with_data=True)
    msg = await message.answer(restart_command_TEXT)
    await save_message(message.from_user.id, msg.message_id)
    await asyncio.sleep(1)
    await base_navigation(message.from_user.id)
