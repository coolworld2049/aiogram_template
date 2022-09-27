from aiogram import types
from aiogram.dispatcher import FSMContext

from config import MESSAGE_DELAY
from core import dp, bot
from data.database.db_api import insert_user, update_user
from keyboards.user.common.common_inline_kb import privacy_policy_message_IK, post_main_menu_message_IK, \
    base_navigation
from states.UserStates import UserStates
from utils.chat_mgmt import delete_message, get_last_message


def reg_start_handlers():
    dp.register_message_handler(bot_navigation, commands=['start'])
    dp.register_callback_query_handler(start_user_registration, lambda c: c.data == f"{c.from_user.id}_start_work")
    dp.register_message_handler(set_name, state=UserStates.set_name)


@dp.message_handler(commands=['start'])
async def bot_navigation(message: types.Message):
    await delete_message(message.from_user.id, await get_last_message(message.from_user.id), MESSAGE_DELAY)
    await base_navigation(message.from_user.id)


# end-'/start'


@dp.callback_query_handler(lambda c: c.data == f"{c.from_user.id}_main_menu")
async def start_user_registration(callback_query: types.CallbackQuery):
    if ...:
        await post_main_menu_message_IK(callback_query.from_user.id)
    else:
        await bot.send_message(callback_query.from_user.id, 'TEXT')
        await UserStates.set_name.set()
    await callback_query.message.delete()


@dp.message_handler(state=UserStates.set_name)
async def set_name(message: types.Message, state: FSMContext):
    await insert_user(message.from_user)
    async with state.proxy():
        check_loopback = message.text not in ['/start', '/set_traveler_bio']
        if not message.text.startswith('/') and not message.text.isdigit() and ' ' in message.text:
            spl = message.text.split(' ')
            await update_user(message.from_user, spl[0], spl[1])
            text = "Данные сохранены"
            await bot.send_message(message.from_user.id, text, reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            await privacy_policy_message_IK(message.from_user.id)
        else:
            await message.answer('Неправильный формат ввода')
        if not check_loopback:
            await state.finish()
            await base_navigation(message.from_user.id)
