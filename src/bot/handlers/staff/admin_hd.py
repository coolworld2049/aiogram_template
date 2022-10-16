from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.filters.callback_filters import back_cb
from bot.filters.command_filters import command_admin
from bot.keyboards.staff.admin_kb import admin_panel_message_IK, itemManagerModel, admin_panel_ADD_item, \
    admin_panel_UPDATE_item, admin_panel_DELETE_item
from bot.states.ItemMgmtStates import ItemMgmtStates
from core import dispatcher


def reg_admin_handlers():
    dispatcher.register_message_handler(admin_panel_message_IK, command_admin)
    dispatcher.register_callback_query_handler(admin_panel_back, back_cb.filter(to='admin'))
    dispatcher.register_message_handler(add_item_hd, state=ItemMgmtStates.ADD)
    dispatcher.register_message_handler(update_item_hd, state=ItemMgmtStates.UPDATE)
    dispatcher.register_message_handler(delete_item_hd, state=ItemMgmtStates.DELETE)


@dispatcher.message_handler(command_admin)
async def admin_panel(message: types.Message):
    await admin_panel_message_IK(message.from_user.id)


@dispatcher.callback_query_handler(back_cb.filter(to='admin'))
async def admin_panel_back(message: types.Message):
    await admin_panel_message_IK(message.from_user.id)


@dispatcher.message_handler(state=ItemMgmtStates.ADD)
async def add_item_hd(message: types.Message, state: FSMContext):
    await itemManagerModel.add_item(message, state, admin_panel_ADD_item)


@dispatcher.message_handler(state=ItemMgmtStates.UPDATE)
async def update_item_hd(message: types.Message, state: FSMContext):
    await itemManagerModel.update_item(message, state, admin_panel_UPDATE_item)


@dispatcher.message_handler(state=ItemMgmtStates.DELETE)
async def delete_item_hd(message: types.Message, state: FSMContext):
    await itemManagerModel.delete_item(message, state, admin_panel_DELETE_item)
