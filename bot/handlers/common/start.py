from aiogram import types
from loguru import logger

from bot.filters.commands import command_start
from bot.keyboards.user.common.common_inline_kb import base_navigation
from bot.utils.chat_mgmt import delete_previous_messages
from core import dispatcher


def reg_start_handlers():
    dispatcher.register_message_handler(start, command_start)


@dispatcher.message_handler(command_start)
async def start(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await base_navigation(message.from_user.id)
    logger.info(f"user_id: {message.from_user.id}")



