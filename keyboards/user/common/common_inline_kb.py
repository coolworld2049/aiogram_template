import typing

from aiogram import types

from config import MESSAGE_DELAY, privacy_policy_LINK
from core import bot, logger
from data.database.database import fetchone
from data.database.db_api import fetchone_user
from keyboards.user.common.common_reply_kb import RK_verify_phone
from utils.chat_mgmt import save_message, delete_message, get_last_message


async def base_navigation(user_id: int):
    if ...:
        await main_menu_message_IK(user_id)
    elif ...:
        await registration_menu_message_IK(user_id)
    else:
        _agree_with_rules = await fetchone('''SELECT agree_with_rules FROM bot.user WHERE user_id = $1''', [user_id])
        if len(_agree_with_rules) > 0:
            await main_menu_message_IK(user_id)
        else:
            await privacy_policy_message_IK(user_id)


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
        await delete_message(user_id, await get_last_message(user_id), message_del_delay)
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
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    text = 'Чтобы начать пользоваться сервисом, Вам нужно пройти регистрацию.'
    IK = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton('Пройти регистрацию', callback_data=f"{user_id}_main_menu"))
    message = await bot.send_message(user_id, text, reply_markup=IK)
    await save_message(user_id, message.message_id)


async def privacy_policy_message_IK(user_id: int):
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    IK = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('👍 Прочитал, согласен!', callback_data=f"{user_id}_agree-with-rules_True"),
        types.InlineKeyboardButton('😔 Не согласен!', callback_data=f"{user_id}_agree-with-rules_False"))
    text = f"Согласие на обработку персональных данных: {privacy_policy_LINK}"
    message = await bot.send_message(user_id, text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=IK,
                                     disable_web_page_preview=True)
    await save_message(user_id, message.message_id)


async def phone_verification_message_IK(user_id: int):
    try:
        user = await fetchone_user(user_id)
        if len(user) > 0 and not user['phone']:
            await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
            text = """Вам необходимо подтвердить номер мобильного телефона"""
            message = await bot.send_message(user_id, text, reply_markup=RK_verify_phone(),
                                             parse_mode=types.ParseMode.MARKDOWN)
            await save_message(user_id, message.message_id)
            ...
        else:
            return True
    except KeyError:
        logger.error(f"phone_verification_message_IK: user_id: {user_id}: user does not exist in 'user' table")
        await base_navigation(user_id)


async def main_menu_message_IK(user_id: int):
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    text = """Вы находитесь в главном меню
    
..."""
    IK = types.InlineKeyboardMarkup(row_width=2) \
        .add(types.InlineKeyboardButton('👤 Мой аккаунт', callback_data=f"{user_id}_my-account"))
    message = await bot.send_message(user_id, text, reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
    await save_message(user_id, message.message_id)


async def post_main_menu_message_IK(user_id: int):
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    text = """2 уровень меню"""
    IK = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton('...', callback_data=f"{user_id}_' '"),
        types.InlineKeyboardButton('👈 Назад', callback_data=f"{user_id}_back-to-menu"))
    message = await bot.send_message(user_id, text, reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
    await save_message(user_id, message.message_id)


async def account_message_IK(user_id: int):
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    user = await fetchone_user(user_id)
    account_text = f"""😇 Это Ваш аккаунт.

👤 *Имя*: {user['first_name']} {user['last_name']}

*ID*: {user['user_id']}

..."""
    IK = types.InlineKeyboardMarkup(row_width=2)
    IK.row(types.InlineKeyboardButton('👈 Назад', callback_data=f"{user_id}_back-to-menu"))
    message = await bot.send_message(user_id, account_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=IK)
    await save_message(user_id, message.message_id)


async def cancel_button_IK(order_id: int, get_btn_callback_data=False):
    cb = f"{order_id}_cancel-flight-route"
    if not get_btn_callback_data:
        return types.InlineKeyboardButton('❌ Отмена', callback_data=cb)
    else:
        return cb
