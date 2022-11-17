import asyncio

from aiogram import types
from loguru import logger

from bot.filters.commands import command_reload
from bot.keyboards.user.common_inline_kb import base_navigation
from bot.strings.locale import restart_command_TEXT
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from core import dispatcher


def reg_restart_handlers():
    dispatcher.register_message_handler(restart, command_reload, state='*')


async def reset_state(message: types.Message, text: str):
    await delete_previous_messages(tgtype=message)
    await dispatcher.current_state(chat=message.from_user.id, user=message.from_user.id).reset_state(with_data=True)
    msg = await message.answer(text)
    await save_message(message.from_user.id, msg.message_id)


@dispatcher.message_handler(command_reload, state='*')
async def restart(message: types.Message):
    await reset_state(message, restart_command_TEXT)
    await asyncio.sleep(1)
    await base_navigation(message.from_user.id)
    logger.info(f"user_id: {message.from_user.id}")
