import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import config
from bot.filters.callbacks import item_cb, server_stats_cb
from bot.filters.commands import command_admin
from bot.keyboards.employees.common.user_mgmt import post_user_mgmt_message_IK
from bot.models.item.model import ItemManagerModel
from bot.models.role.role import UserRole
from bot.models.verify.model import verifyUserModel
from bot.strings.locale import admin_panel_BTN_items_mgmt_TEXT, admin_panel_TEXT, \
    admin_panel_BTN_server_stats_TEXT
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from bot.config import MESSAGE_DELAY
from core import bot


async def pre_admin_panel_message_IK(user_id: int, role: UserRole):
    async def _panel():
        cb = item_cb.new(action='None', callback=command_admin.commands[0], role=role)
        btn_panel = types.InlineKeyboardButton(admin_panel_BTN_items_mgmt_TEXT, callback_data=cb)
        btn_server_stats = types.InlineKeyboardButton(admin_panel_BTN_server_stats_TEXT,
                                                      callback_data=server_stats_cb.new())
        IK = types.InlineKeyboardMarkup().add(btn_panel, btn_server_stats)
        msg = await bot.send_message(user_id, admin_panel_TEXT, reply_markup=IK)
        await save_message(user_id, msg.message_id)

    verify_result = await verifyUserModel.verify(user_id)
    if verify_result['role'] == UserRole.ADMIN or verify_result['user_id'] in config.ADMINS:
        await delete_previous_messages(user_id)
        await _panel()
    else:
        await delete_previous_messages(user_id)
        msg_error = await bot.send_message(user_id, 'No access')
        await save_message(user_id, msg_error.message_id)


itemManagerModel_admin = ItemManagerModel(pre_admin_panel_message_IK, post_user_mgmt_message_IK)


async def admin_panel_ADD_item_func(message: types.Message, state: FSMContext):
    msg = await message.answer('changes saved')
    await save_message(message.from_user.id, msg.message_id)
    await asyncio.sleep(MESSAGE_DELAY)


async def admin_panel_UPDATE_item_func(message: types.Message, state: FSMContext):
    msg = await message.answer('changes saved')
    await save_message(message.from_user.id, msg.message_id)
    await asyncio.sleep(MESSAGE_DELAY)


async def admin_panel_DELETE_item_func(message: types.Message, state: FSMContext):
    msg = await message.answer('changes saved')
    await save_message(message.from_user.id, msg.message_id)
    await asyncio.sleep(MESSAGE_DELAY)
