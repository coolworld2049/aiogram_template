from aiogram import types

from bot.answer_blanks.lang import admin_panel_BTN_TEXT, admin_panel_TEXT, navigation_BTN_back, \
    navigation_BTN_back_to_menu, items_mgmt_message_IK_TEXT, items_mgmt_message_IK_TEXT_error
from bot.filters.callback_filters import item_cb, back_cb
from bot.filters.command_filters import command_admin
from bot.models.item.model import ItemManagerModel
from bot.models.verify import verifyUserModel
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from bot.utils.pgdbapi import fetchone_user, fetchall_user
from core import bot


async def admin_panel_message_IK(user_id: int):
    async def _panel():
        await delete_previous_messages(user_id)
        IK = types.InlineKeyboardMarkup() \
            .add(types.InlineKeyboardButton(admin_panel_BTN_TEXT,
                                            callback_data=item_cb.new(action='None',
                                                                      callback=command_admin.commands[0])))
        msg = await bot.send_message(user_id, admin_panel_TEXT, reply_markup=IK)
        await save_message(user_id, msg.message_id)

    user = await fetchone_user(user_id)
    if user['is_admin'] in (None, False):
        await delete_previous_messages(user_id)
        verify_result = await verifyUserModel.verify(user_id)
        if verify_result['is_admin']:
            await _panel()
    else:
        await _panel()


async def user_mgmt_message_IK(user_id: int):
    await delete_previous_messages(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    example_items = await fetchall_user()
    if example_items and len(example_items) > 0:
        for ex_item in example_items:
            data = f"[{ex_item['username']}] admin: {ex_item['is_admin']}, manager: {ex_item['is_manager']}"
            item_callback = f"{ex_item['user_id']}"
            IK.insert(types.InlineKeyboardButton(data, callback_data=item_cb.new(action='update',
                                                                                 callback=item_callback)))
        IK.row(types.InlineKeyboardButton('➕', callback_data=item_cb.new(action='add', callback='None')),
               types.InlineKeyboardButton('➖', callback_data=item_cb.new(action='delete', callback='None')))
        IK.row(types.InlineKeyboardButton(navigation_BTN_back,
                                          callback_data=back_cb.new(to='admin-panel', msg_ids='None')))
        IK.row(types.InlineKeyboardButton(navigation_BTN_back_to_menu,
                                          callback_data=back_cb.new(to='menu', msg_ids='None')))
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT,
                                         reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
        await save_message(user_id, message.message_id)
    else:
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT_error, reply_markup=IK)
        await save_message(user_id, message.message_id)


async def admin_panel_ADD_item():
    print('admin_panel_ADD_item')


async def admin_panel_UPDATE_item():
    print('admin_panel_UPDATE_item')


async def admin_panel_DELETE_item():
    print('admin_panel_DELETE_item')


itemManagerModel = ItemManagerModel(admin_panel_message_IK, user_mgmt_message_IK)
