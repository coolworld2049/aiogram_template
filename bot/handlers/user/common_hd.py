from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.filters.callbacks import common_cb, back_cb
from bot.filters.callbacks import reg_user_cb
from bot.filters.commands import command_start
from bot.keyboards.user.common_inline_kb import account_menu_message_IK
from bot.keyboards.user.common_inline_kb import base_navigation, main_menu_message_IK
from bot.states.UserStates import UserStates
from bot.strings.locale import user_registration_TEXT, user_state_finish_TEXT, user_state_incorrect_input_TEXT, \
    user_state_incorrect_input_TEXT_delimeter_error
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from bot.models.database.postgresql.api import insert_user, update_user
from core import dispatcher, bot


def reg_common_handlers():
    dispatcher.register_callback_query_handler(user_registration, reg_user_cb.filter(), state='*')
    dispatcher.register_message_handler(set_name, state=UserStates.SET_NAME)
    dispatcher.register_callback_query_handler(account, common_cb.filter(), state='*')
    dispatcher.register_callback_query_handler(back_to_account, back_cb.filter(to='account'), state='*')
    dispatcher.register_callback_query_handler(back_to_menu, back_cb.filter(to='menu'), state='*')


@dispatcher.callback_query_handler(reg_user_cb.filter(), state='*')
async def user_registration(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await bot.send_message(callback_query.from_user.id, user_registration_TEXT)
    await UserStates.SET_NAME.set()
    logger.info(f"user_id: {callback_query.from_user.id}")


@dispatcher.message_handler(state=UserStates.SET_NAME)
async def set_name(message: types.Message, state: FSMContext):
    await delete_previous_messages(tgtype=message)
    await insert_user(message.from_user)
    async with state.proxy():
        if not message.text.startswith('/') and not message.text.isdigit() and ' ' in message.text:
            spl = message.text.split(' ')
            await update_user(message.from_user, spl[0], spl[1])
            msg = await bot.send_message(message.from_user.id, user_state_finish_TEXT,
                                         reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            await main_menu_message_IK(message.from_user.id)
        elif ' ' not in message.text:
            msg = await message.answer(user_state_incorrect_input_TEXT_delimeter_error)
        else:
            msg = await message.answer(user_state_incorrect_input_TEXT)
        if await command_start.check(message):
            await state.finish()
            await base_navigation(message.from_user.id)
        await save_message(message.from_user.id, msg.message_id)


@dispatcher.callback_query_handler(common_cb.filter(), state='*')
async def account(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await account_menu_message_IK(callback_query.from_user.id)
    logger.info(f"user_id: {callback_query.from_user.id}")


@dispatcher.callback_query_handler(back_cb.filter(to='account'), state='*')
async def back_to_account(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await account_menu_message_IK(callback_query.from_user.id)


@dispatcher.callback_query_handler(back_cb.filter(to='menu'), state='*')
async def back_to_menu(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await main_menu_message_IK(callback_query.from_user.id)
