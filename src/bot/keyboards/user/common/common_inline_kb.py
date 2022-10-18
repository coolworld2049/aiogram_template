import typing

from aiogram import types

from bot.config import MESSAGE_DELAY
from bot.strings.answer_blanks import registration_menu_TEXT, main_menu_TEXT, account_menu_message_IK_TEXT, navigation_menu_TEXT, \
    navigation_BTN_back, navigation_BTN_back_to_menu, registration_menu_message_IK_TEXT, \
    main_menu_message_IK_BTN_account_TEXT
from core import bot
from database.postgresql.api import fetchone_user
from bot.filters.callback_filters import back_cb, reg_user_cb, common_cb
from helpers.bot.chat_mgmt import save_message, delete_message_handler, get_last_message


async def base_navigation(user_id: int):
    await delete_message_handler(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    user = await fetchone_user(user_id)
    if user and user['first_name'] and user['last_name']:
        await main_menu_message_IK(user_id)
    else:
        await registration_menu_message_IK(user_id)


async def navigation_menu(user_id: int, custom_cb: str = None, direction: str = None,
                          messages_id: str = None, delete_yourself: bool = True,
                          message_del_delay: int | float = MESSAGE_DELAY,
                          func: typing.Any = None,
                          *args: typing.Any):
    """
    callback_data=f"{user_id}_back-to-{back_to}_{messages_id if messages_id else ''}"\n
    callback_data=f"{user_id}_back-to-menu_{messages_id if messages_id else ''}"\n
    set func or cb
    :param delete_yourself:
    :param message_del_delay:
    :param func: run func
    :param user_id:
    :param custom_cb: custom callback_data
    :param direction: 'menu' or 'account' or None
    :param messages_id:
    :return:
    """
    if delete_yourself:
        await delete_message_handler(user_id, await get_last_message(user_id), message_del_delay)
    IK_back = types.InlineKeyboardMarkup()
    if direction:
        bk_cb = back_cb.new(to=direction, msg_ids=messages_id if messages_id else None)
        IK_back.insert(types.InlineKeyboardButton(navigation_BTN_back, callback_data=bk_cb))
    if custom_cb:
        cs_bk_cb = back_cb.new(to=custom_cb, msg_ids=messages_id if messages_id else None)
        IK_back.insert(types.InlineKeyboardButton(navigation_BTN_back, callback_data=cs_bk_cb))
    if func and args:
        func(*args)
    elif func:
        func()
    menu_bk_cb = back_cb.new(to='menu', msg_ids=messages_id if messages_id else None)
    IK_back.insert(types.InlineKeyboardButton(navigation_BTN_back_to_menu,
                                              callback_data=menu_bk_cb))
    message = await bot.send_message(user_id, navigation_menu_TEXT, parse_mode=types.ParseMode.MARKDOWN,
                                     reply_markup=IK_back)
    if delete_yourself:
        await save_message(user_id, message.message_id)


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
