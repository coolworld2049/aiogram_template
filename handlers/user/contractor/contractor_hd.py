import asyncio

from aiogram import types
from keyboards.user.contractor.contractor_kb import contractor_account_message_IK

from config import MESSAGE_DELAY
from core import dp
from utils.chat_mgmt import delete_message


def reg_customer_handlers():
    dp.register_callback_query_handler(contractor_account,
                                       lambda c: str(c.data).split('_')[1] == "contractor-account", state='*')


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == "contractor-account", state='*')
async def contractor_account(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    if msg_ids:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
        await delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
    else:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
    await contractor_account_message_IK(callback_query.from_user.id)
