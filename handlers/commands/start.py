from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from config import MESSAGE_DELAY
from core import dp, bot
from data.database.db_api import save_user, update_user
from keyboards.user.common.common_inline_kb import base_navigation, main_menu_message_IK
from states.UserStates import UserStates
from utils.chat_mgmt import del_message, get_last_message


def reg_start_handlers():
    dp.register_message_handler(start, CommandStart())
    dp.register_callback_query_handler(user_registration, lambda c: c.data == f"{c.from_user.id}_reg-user")
    dp.register_message_handler(set_name, state=UserStates.set_name)


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await del_message(message.from_user.id, await get_last_message(message.from_user.id), MESSAGE_DELAY)
    await base_navigation(message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == f"{c.from_user.id}_reg-user")
async def user_registration(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите ваше Имя Фамилия (Пример: Иван Иванов)')
    await UserStates.set_name.set()


@dp.message_handler(state=UserStates.set_name)
async def set_name(message: types.Message, state: FSMContext):
    await save_user(message.from_user)
    async with state.proxy():
        check_loopback = message.text != '/start'
        if not message.text.startswith('/') and not message.text.isdigit() and ' ' in message.text:
            spl = message.text.split(' ')
            await update_user(message.from_user, spl[0], spl[1])
            text = "Данные сохранены"
            await bot.send_message(message.from_user.id, text, reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            await main_menu_message_IK(message.from_user.id)
        else:
            await message.answer('Неправильный формат ввода')
        if not check_loopback:
            await state.finish()
            await base_navigation(message.from_user.id)
