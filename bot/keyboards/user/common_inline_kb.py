from aiogram import types

from bot.config import MESSAGE_DELAY
from bot.filters.callbacks import back_cb, reg_user_cb, common_cb
from bot.models.database.postgresql.api import fetchone_user
from bot.strings.locale import registration_menu_TEXT, main_menu_TEXT, account_menu_message_IK_TEXT, \
    navigation_BTN_back, registration_menu_message_IK_TEXT, \
    main_menu_message_IK_BTN_account_TEXT
from bot.utils.chat_mgmt import save_message, delete_message_handler, get_last_message
from core import bot


async def base_navigation(user_id: int):
    await delete_message_handler(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    user = await fetchone_user(user_id)
    if user and user['first_name'] and user['last_name']:
        await main_menu_message_IK(user_id)
    else:
        await registration_menu_message_IK(user_id)


async def registration_menu_message_IK(user_id: int):
    await delete_message_handler(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    IK = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton(registration_menu_message_IK_TEXT, callback_data=reg_user_cb.new()))
    message = await bot.send_message(user_id, registration_menu_TEXT, reply_markup=IK)
    await save_message(user_id, message.message_id)


async def main_menu_message_IK(user_id: int):
    await delete_message_handler(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    IK = types.InlineKeyboardMarkup(row_width=2) \
        .add(types.InlineKeyboardButton(main_menu_message_IK_BTN_account_TEXT, callback_data=common_cb.new()))
    message = await bot.send_message(user_id, main_menu_TEXT, reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
    await save_message(user_id, message.message_id)


async def account_menu_message_IK(user_id: int):
    await delete_message_handler(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    user = await fetchone_user(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    IK.row(types.InlineKeyboardButton(navigation_BTN_back, callback_data=back_cb.new(to='menu', msg_ids='None')))
    message = await bot.send_message(user_id, account_menu_message_IK_TEXT(user) if user else None,
                                     parse_mode=types.ParseMode.MARKDOWN, reply_markup=IK)
    await save_message(user_id, message.message_id)
