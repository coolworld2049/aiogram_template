from aiogram import types
from aiogram.dispatcher import FSMContext

from config import user_registration_TEXT, user_state_finish_TEXT
from core import dp, bot
from models.database.db_api import save_user, update_user
from filters.callback_filters import reg_user_cb
from filters.command_filters import command_start
from keyboards.user.common.common_inline_kb import base_navigation, main_menu_message_IK
from states.UserStates import UserStates
from utils.chat_mgmt import delete_previous_messages


def reg_start_handlers():
    dp.register_message_handler(start, command_start)
    dp.register_callback_query_handler(user_registration, reg_user_cb.filter())
    dp.register_message_handler(set_name, state=UserStates.set_name)


@dp.message_handler(command_start)
async def start(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await base_navigation(message.from_user.id)


@dp.callback_query_handler(reg_user_cb.filter())
async def user_registration(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await bot.send_message(callback_query.from_user.id, user_registration_TEXT)
    await UserStates.set_name.set()


@dp.message_handler(state=UserStates.set_name)
async def set_name(message: types.Message, state: FSMContext):
    await delete_previous_messages(tgtype=message)
    await save_user(message.from_user)
    async with state.proxy():
        if not message.text.startswith('/') and not message.text.isdigit() and ' ' in message.text:
            spl = message.text.split(' ')
            await update_user(message.from_user, spl[0], spl[1])
            await bot.send_message(message.from_user.id, user_state_finish_TEXT,
                                   reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            await main_menu_message_IK(message.from_user.id)
        else:
            await message.answer('Неправильный формат ввода')
        if message.get_command() == '/start':
            await state.finish()
            await base_navigation(message.from_user.id)
