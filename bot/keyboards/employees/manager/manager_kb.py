from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import config
from bot.filters.callback_filters import item_cb
from bot.filters.command_filters import command_manager
from bot.keyboards.employees.common.user_mgmt import post_user_mgmt_message_IK
from bot.models.item.model import ItemManagerModel
from bot.models.role.role import UserRole
from bot.models.verify import verifyUserModel
from bot.strings.locale import manager_panel_BTN_items_mgmt_TEXT, manager_panel_TEXT
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from core import bot


async def pre_manager_panel_message_IK(user_id: int, role: UserRole):

    async def _panel():
        cb = item_cb.new(action='None', callback=command_manager.commands[0], role=role)
        btn_panel = types.InlineKeyboardButton(manager_panel_BTN_items_mgmt_TEXT, callback_data=cb)
        IK = types.InlineKeyboardMarkup().add(btn_panel)
        msg = await bot.send_message(user_id, manager_panel_TEXT, reply_markup=IK)
        await save_message(user_id, msg.message_id)

    verify_result = await verifyUserModel.verify(user_id)
    if verify_result['role'] == UserRole.MANAGER or verify_result['user_id'] in config.MANAGERS:
        await delete_previous_messages(user_id)
        await _panel()
    else:
        await bot.send_message(user_id)

itemManagerModel_manager = ItemManagerModel(pre_manager_panel_message_IK, post_user_mgmt_message_IK)


async def manager_panel_ADD_item_func(message: types.Message, state: FSMContext):
    ...
    print('manager_panel_ADD_item')


async def manager_panel_UPDATE_item_func(message: types.Message, state: FSMContext):
    ...
    print('manager_panel_UPDATE_item')


async def manager_panel_DELETE_item_func(message: types.Message, state: FSMContext):
    ...
    print('manager_panel_DELETE_item')
