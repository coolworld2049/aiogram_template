import typing

from aiogram import types

from config import MESSAGE_DELAY, registration_menu_TEXT, main_menu_TEXT
from core import bot
from data.database.db_api import fetchone_user
from utils.chat_mgmt import save_message, del_message, get_last_message


async def base_navigation(user_id: int):
    user = await fetchone_user(user_id)
    if user and user['first_name'] and user['last_name']:
        await main_menu_message_IK(user_id)
    else:
        await registration_menu_message_IK(user_id)


async def navigation_menu(user_id: int, cb: str = None, back_to: str = None,
                          messages_id: str = None, delete_yourself: bool = True,
                          message_del_delay: int | float = MESSAGE_DELAY,
                          func: typing.Any = None,
                          *args: typing.Any):
    """
    callback_data=f"{user_id}_back-to-{back_to}_{messages_id if messages_id else ''}"
    callback_data=f"{user_id}_back-to-menu_{messages_id if messages_id else ''}"
    set func or cb
    :param delete_yourself:
    :param message_del_delay:
    :param func: run func
    :param user_id:
    :param cb: custom callback_data
    :param back_to: 'menu' or 'account' or None
    :param messages_id:
    :return:
    """
    if delete_yourself:
        await del_message(user_id, await get_last_message(user_id), message_del_delay)
    IK_back = types.InlineKeyboardMarkup()
    if back_to:
        back_cb = f"{user_id}_back-to-{back_to}_{messages_id if messages_id else ''}"
        IK_back.insert(types.InlineKeyboardButton('👈 Назад', callback_data=back_cb))
    if cb:
        cb_data = f"{cb}_{messages_id if messages_id else ''}"
        IK_back.insert(types.InlineKeyboardButton('👈 Назад', callback_data=cb_data))
    if func and args:
        func(*args)
    elif func:
        func()
    IK_back.insert(types.InlineKeyboardButton('👈️ В меню',
                                              callback_data=f"{user_id}_back-to-menu_{messages_id if messages_id else ''}"))
    message = await bot.send_message(user_id, 'Навигация', parse_mode=types.ParseMode.MARKDOWN, reply_markup=IK_back)
    if delete_yourself:
        await save_message(user_id, message.message_id)


async def registration_menu_message_IK(user_id: int):
    await del_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    IK = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton('Регистрация', callback_data=f"{user_id}_reg-user"))
    message = await bot.send_message(user_id, registration_menu_TEXT, reply_markup=IK)
    await save_message(user_id, message.message_id)


async def main_menu_message_IK(user_id: int):
    await del_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    IK = types.InlineKeyboardMarkup(row_width=2) \
        .add(types.InlineKeyboardButton('👤 Мой аккаунт', callback_data=f"{user_id}_my-account"))
    message = await bot.send_message(user_id, main_menu_TEXT, reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
    await save_message(user_id, message.message_id)


async def account_menu_message_IK(user_id: int):
    await del_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    user = await fetchone_user(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    IK.row(types.InlineKeyboardButton('👈 Назад', callback_data=f"{user_id}_back-to-menu"))
    account_text = '...'
    if user:
        account_text = f"""Ваш аккаунт.
    
*Имя*: {user['first_name']} {user['last_name']}
*ID*: {user['user_id']}"""
    message = await bot.send_message(user_id, account_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=IK)
    await save_message(user_id, message.message_id)
