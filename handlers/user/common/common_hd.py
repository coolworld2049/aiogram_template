from aiogram import types

from core import dp
from keyboards.user.common.common_inline_kb import account_menu_message_IK, \
    main_menu_message_IK
from utils.chat_mgmt import delete_previous_messages


def reg_common_interface_handlers():
    dp.register_callback_query_handler(my_account,
                                       lambda c: str(c.data).split('_')[1] == f"{c.from_user.id}_my-account", state='*')
    dp.register_callback_query_handler(back_to_account,
                                       lambda c: str(c.data).split('_')[1] == f"back-to-account", state='*')
    dp.register_callback_query_handler(back_to_menu,
                                       lambda c: str(c.data).split('_')[1] == f"back-to-menu", state='*')


@dp.callback_query_handler(lambda c: c.data == f"{c.from_user.id}_my-account", state='*')
async def my_account(callback_query: types.CallbackQuery):
    await account_menu_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == f"back-to-account", state='*')
async def back_to_account(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    await delete_previous_messages(msg_ids, callback_query)
    await account_menu_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == f"back-to-menu", state='*')
async def back_to_menu(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    await delete_previous_messages(msg_ids, callback_query)
    await main_menu_message_IK(callback_query.from_user.id)
