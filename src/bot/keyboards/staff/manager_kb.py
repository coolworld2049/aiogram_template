from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import config
from bot.filters.callback_filters import item_cb, back_cb
from bot.filters.command_filters import command_manager
from bot.keyboards.user.common.common_inline_kb import base_navigation
from bot.models.item.model import ItemManagerModel
from bot.models.role.role import UserRole
from bot.models.verify import verifyUserModel
from bot.strings.answer_blanks import manager_panel_BTN_items_mgmt_TEXT, manager_panel_TEXT, navigation_BTN_back, \
    items_mgmt_message_IK_TEXT, items_mgmt_message_IK_TEXT_error
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from bot.utils.pgdbapi import fetchall_user
from core import bot


async def pre_manager_panel_message_IK(user_id: int):
    await delete_previous_messages(user_id)

    async def _panel():
        cb = item_cb.new(action='None', callback=command_manager.commands[0])
        btn_panel = types.InlineKeyboardButton(manager_panel_BTN_items_mgmt_TEXT, callback_data=cb)
        IK = types.InlineKeyboardMarkup().add(btn_panel)
        msg = await bot.send_message(user_id, manager_panel_TEXT, reply_markup=IK)
        await save_message(user_id, msg.message_id)

    verify_result = await verifyUserModel.verify(user_id)
    if verify_result['role'] == UserRole.MANAGER or verify_result['user_id'] in config.MANAGERS:
        await _panel()


async def post_user_mgmt_message_IK_manager(user_id: int):
    await delete_previous_messages(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    users = await fetchall_user()
    if users and len(users) > 0:
        for user in users:
            text = f"{user['user_id']} | username: {user['username']} | role: {user['role']}"
            item_callback = f"{user_id}_edit_{user['user_id']}"
            IK.insert(types.InlineKeyboardButton(text, callback_data=item_cb.new(action='update',
                                                                                 callback=item_callback)))
        IK.row(types.InlineKeyboardButton('➕', callback_data=item_cb.new(action='add', callback='None')),
               types.InlineKeyboardButton('➖', callback_data=item_cb.new(action='delete', callback='None')))
        IK.row(types.InlineKeyboardButton(navigation_BTN_back,
                                          callback_data=back_cb.new(to=UserRole.MANAGER, msg_ids='None')))
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT, reply_markup=IK,
                                         parse_mode=types.ParseMode.MARKDOWN)
        await save_message(user_id, message.message_id)
    else:
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT_error, reply_markup=IK)
        await save_message(user_id, message.message_id)


itemManagerModel_manager = ItemManagerModel(pre_manager_panel_message_IK, post_user_mgmt_message_IK_manager)


async def manager_panel_ADD_item_func(message: types.Message, state: FSMContext):
    print('manager_panel_ADD_item')


async def manager_panel_UPDATE_item_func(message: types.Message, state: FSMContext):
    print('manager_panel_UPDATE_item')


async def manager_panel_DELETE_item_func(message: types.Message, state: FSMContext):
    print('manager_panel_DELETE_item')
