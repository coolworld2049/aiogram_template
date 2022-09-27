import asyncio

from aiogram import types

from config import MESSAGE_DELAY
from core import dp
from keyboards.user.customer.customer_kb import customer_account_message_IK
from utils.chat_mgmt import delete_message


def reg_contractor_handlers():
    dp.register_callback_query_handler(customer_account,
                                       lambda c: str(c.data).split('_')[1] == "customer-account", state='*')


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == f"customer-account", state='*')
async def customer_account(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    if msg_ids:
        await delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
    else:
        await asyncio.sleep(MESSAGE_DELAY)
        await callback_query.message.delete()
    await customer_account_message_IK(callback_query.from_user.id)


