from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.models.role.role import UserRole
from bot.strings.answer_blanks import admin_panel_BTN_items_mgmt_TEXT, admin_panel_TEXT, navigation_BTN_back, \
    items_mgmt_message_IK_TEXT, items_mgmt_message_IK_TEXT_error, \
    admin_panel_BTN_server_stats_TEXT
from bot.filters.callback_filters import item_cb, back_cb, server_stats_cb
from bot.filters.command_filters import command_admin
from bot.keyboards.user.common.common_inline_kb import base_navigation
from bot.models.item.model import ItemManagerModel
from bot.models.verify import verifyUserModel
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from bot.utils.pgdbapi import fetchall_user
from core import bot


async def pre_admin_panel_message_IK(user_id: int):
    await delete_previous_messages(user_id)

    async def _panel():
        cb = item_cb.new(action='None', callback=command_admin.commands[0])
        btn_adm_panel = types.InlineKeyboardButton(admin_panel_BTN_items_mgmt_TEXT, callback_data=cb)
        btn_server_stats = types.InlineKeyboardButton(admin_panel_BTN_server_stats_TEXT,
                                                      callback_data=server_stats_cb.new())
        IK = types.InlineKeyboardMarkup().add(btn_adm_panel, btn_server_stats)
        msg = await bot.send_message(user_id, admin_panel_TEXT, reply_markup=IK)
        await save_message(user_id, msg.message_id)

    verify_result = await verifyUserModel.verify(user_id)
    if verify_result['role'] == UserRole.ADMIN:
        await _panel()
    else:
        await base_navigation(user_id)


async def post_user_mgmt_message_IK(user_id: int):
    await delete_previous_messages(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    example_items = await fetchall_user()
    if example_items and len(example_items) > 0:
        for ex_item in example_items:
            text = f"[{ex_item['username']}] admin: {ex_item['is_admin']}, manager: {ex_item['is_manager']}"
            item_callback = ex_item['user_id']
            IK.insert(types.InlineKeyboardButton(text, callback_data=item_cb.new(action='update',
                                                                                 callback=item_callback)))
        IK.row(types.InlineKeyboardButton('➕', callback_data=item_cb.new(action='add', callback='None')),
               types.InlineKeyboardButton('➖', callback_data=item_cb.new(action='delete', callback='None')))
        IK.row(types.InlineKeyboardButton(navigation_BTN_back,
                                          callback_data=back_cb.new(to=UserRole.ADMIN, msg_ids='None')))
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT,
                                         reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
        await save_message(user_id, message.message_id)
    else:
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT_error, reply_markup=IK)
        await save_message(user_id, message.message_id)


itemManagerModel_admin = ItemManagerModel(pre_admin_panel_message_IK, post_user_mgmt_message_IK)


async def admin_panel_PICK_item_func(user_id: int):
    await delete_previous_messages(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    example_items = await fetchall_user()
    if example_items and len(example_items) > 0:
        for ex_item in example_items:
            text = f"[{ex_item['username']}] admin: {ex_item['is_admin']}, manager: {ex_item['is_manager']}"
            item_callback = ex_item['user_id']
            IK.insert(types.InlineKeyboardButton(text, callback_data=item_cb.new(action='update',
                                                                                 callback=item_callback)))
        IK.row(types.InlineKeyboardButton('➕', callback_data=item_cb.new(action='add', callback='None')),
               types.InlineKeyboardButton('➖', callback_data=item_cb.new(action='delete', callback='None')))
        IK.row(types.InlineKeyboardButton(navigation_BTN_back,
                                          callback_data=back_cb.new(to=UserRole.ADMIN, msg_ids='None')))
        msg = await bot.send_message(user_id, items_mgmt_message_IK_TEXT,
                                     reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
        await save_message(user_id, msg.message_id)
    else:
        msg = await bot.send_message(user_id, items_mgmt_message_IK_TEXT_error, reply_markup=IK)
        await save_message(user_id, msg.message_id)


async def admin_panel_ADD_item_func(message: types.Message, state: FSMContext):
    print('admin_panel_ADD_item')


async def admin_panel_UPDATE_item_func(message: types.Message, state: FSMContext):
    print('admin_panel_UPDATE_item')


async def admin_panel_DELETE_item_func(message: types.Message, state: FSMContext):
    print('admin_panel_DELETE_item')
