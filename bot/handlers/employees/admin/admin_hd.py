from aiogram import types
from loguru import logger

from bot.filters.callback_filters import back_cb
from bot.filters.command_filters import command_admin
from bot.keyboards.employees.admin.admin_kb import pre_admin_panel_message_IK
from bot.models.role.role import UserRole
from core import dispatcher


def reg_admin_handlers():
    dispatcher.register_message_handler(pre_admin_panel_message_IK, command_admin)
    dispatcher.register_callback_query_handler(admin_panel_back, back_cb.filter(to=UserRole.ADMIN))


@dispatcher.message_handler(command_admin)
async def admin_panel(message: types.Message):
    await pre_admin_panel_message_IK(message.from_user.id, UserRole.ADMIN)
    logger.info(f"user_id: {message.from_user.id} is {UserRole.ADMIN}")


@dispatcher.callback_query_handler(back_cb.filter(to=UserRole.ADMIN))
async def admin_panel_back(callback_query: types.CallbackQuery):
    await pre_admin_panel_message_IK(callback_query.from_user.id, UserRole.ADMIN)


