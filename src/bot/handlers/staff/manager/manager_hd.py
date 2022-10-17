from aiogram import types

from bot.filters.callback_filters import back_cb
from bot.filters.command_filters import command_manager
from bot.keyboards.staff.manager.manager_kb import pre_manager_panel_message_IK
from bot.models.role.role import UserRole
from core import dispatcher


def reg_manager_handlers():
    dispatcher.register_message_handler(pre_manager_panel_message_IK, command_manager)
    dispatcher.register_callback_query_handler(manager_panel_back, back_cb.filter(to=UserRole.MANAGER))


@dispatcher.message_handler(command_manager)
async def manager_panel(message: types.Message):
    await pre_manager_panel_message_IK(message.from_user.id, UserRole.MANAGER)


@dispatcher.callback_query_handler(back_cb.filter(to=UserRole.MANAGER))
async def manager_panel_back(message: types.Message):
    await pre_manager_panel_message_IK(message.from_user.id, UserRole.MANAGER)