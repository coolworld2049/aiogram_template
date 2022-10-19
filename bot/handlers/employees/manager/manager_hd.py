from aiogram import types
from loguru import logger

from bot.filters.callback_filters import back_cb
from bot.filters.command_filters import command_manager
from bot.keyboards.employees.manager.manager_kb import pre_manager_panel_message_IK
from bot.models.role.role import UserRole
from core import dispatcher


def reg_manager_handlers():
    dispatcher.register_message_handler(pre_manager_panel_message_IK, command_manager)
    dispatcher.register_callback_query_handler(manager_panel_back, back_cb.filter(to=UserRole.MANAGER))


@dispatcher.message_handler(command_manager)
async def manager_panel(message: types.Message):
    await pre_manager_panel_message_IK(message.from_user.id, UserRole.MANAGER)
    logger.info(f"user_id: {message.from_user.id} is {UserRole.MANAGER}")


@dispatcher.callback_query_handler(back_cb.filter(to=UserRole.MANAGER))
async def manager_panel_back(callback_query: types.CallbackQuery):
    await pre_manager_panel_message_IK(callback_query.from_user.id, UserRole.MANAGER)
