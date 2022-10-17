from aiogram import types

from bot.filters.callback_filters import item_cb, back_cb
from bot.models.role.role import UserRole
from bot.strings.answer_blanks import navigation_BTN_back, items_mgmt_message_IK_TEXT, items_mgmt_message_IK_TEXT_error
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from bot.utils.pgdbapi import fetchall_user
from core import bot


async def post_user_mgmt_message_IK(user_id: int, role: UserRole):
    await delete_previous_messages(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    example_items = await fetchall_user()
    if example_items and len(example_items) > 0:
        for ex_item in example_items:
            if ex_item['user_id'] != user_id:
                text = f"{ex_item['username']} | role: {ex_item['role']}"
                item_callback = f"{user_id}_edit_{ex_item['user_id']}"
                IK.row(types.InlineKeyboardButton(
                    text, callback_data=item_cb.new(action='update', callback=item_callback, role=role)))
        IK.row(types.InlineKeyboardButton('➕', callback_data=item_cb.new(action='add', callback='None', role=role)),
               types.InlineKeyboardButton('➖', callback_data=item_cb.new(action='delete', callback='None', role=role)))
        back_callback = UserRole.ADMIN if role == UserRole.ADMIN else UserRole.MANAGER
        IK.row(types.InlineKeyboardButton(navigation_BTN_back, callback_data=back_cb.new(to=back_callback,
                                                                                         msg_ids='None')))
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT, reply_markup=IK,
                                         parse_mode=types.ParseMode.MARKDOWN)
        await save_message(user_id, message.message_id)
    else:
        message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT_error, reply_markup=IK)
        await save_message(user_id, message.message_id)
