import asyncio

from aiogram import types

from config import MESSAGE_DELAY
from core import dp
from keyboards.user.common.common_inline_kb import post_main_menu_message_IK, account_message_IK, \
    main_menu_message_IK
from utils.chat_mgmt import delete_message


def reg_common_interface_handlers():
    dp.register_callback_query_handler(start_work, lambda c: str(c.data).split('_')[1] == "start-work", state='*')
    dp.register_callback_query_handler(my_account, lambda c: c.data == f"{c.from_user.id}_my-account", state='*')
    dp.register_callback_query_handler(back_to_account,
                                       lambda c: str(c.data).split('_')[1] == f"back-to-account", state='*')
    dp.register_callback_query_handler(back_to_menu,
                                       lambda c: str(c.data).split('_')[1] == f"back-to-menu", state='*')
    dp.register_callback_query_handler(back_to_post_menu,
                                       lambda c: str(c.data).split('_')[1] == f"back-to-post-menu", state='*')


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == "start-work", state='*')
async def start_work(callback_query: types.CallbackQuery):
    await asyncio.sleep(MESSAGE_DELAY)
    await callback_query.message.delete()
    await post_main_menu_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(lambda c: c.data == f"{c.from_user.id}_my-account", state='*')
async def my_account(callback_query: types.CallbackQuery):
    await account_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == f"back-to-account", state='*')
async def back_to_account(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    if msg_ids:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
        await delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
    else:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
    await account_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == f"back-to-menu", state='*')
async def back_to_menu(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    if msg_ids:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
        await delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
    else:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
    await main_menu_message_IK(callback_query.from_user.id)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == f"back-to-post-menu", state='*')
async def back_to_post_menu(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    if msg_ids:
        await delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
    else:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
    await post_main_menu_message_IK(callback_query.from_user.id)