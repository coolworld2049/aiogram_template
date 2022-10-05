from aiogram import types

from core import dp
from filters.callback_filters import common_cb, back_cb
from keyboards.user.common.common_inline_kb import account_menu_message_IK, \
    main_menu_message_IK
from utils.chat_mgmt import delete_previous_messages


def reg_common_handlers():
    dp.register_callback_query_handler(my_account, common_cb.filter(), state='*')
    dp.register_callback_query_handler(back_to_account, back_cb.filter(to='account'), state='*')
    dp.register_callback_query_handler(back_to_menu, back_cb.filter(to='menu'), state='*')


@dp.callback_query_handler(common_cb.filter(), state='*')
async def my_account(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await account_menu_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(back_cb.filter(to='account'), state='*')
async def back_to_account(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await account_menu_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(back_cb.filter(to='menu'), state='*')
async def back_to_menu(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await main_menu_message_IK(callback_query.from_user.id)
