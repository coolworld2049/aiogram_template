from aiogram import types

from core import dp
from filters.callback_filters import customer_cb
from keyboards.user.customer.customer_kb import customer_account_message_IK
from utils.chat_mgmt import delete_previous_messages


def reg_contractor_handlers():
    dp.register_callback_query_handler(customer_account, customer_cb.filter(section='account'), state='*')


@dp.callback_query_handler(customer_cb.filter(section='account'), state='*')
async def customer_account(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    await delete_previous_messages(msg_ids=msg_ids, tgtype=callback_query)
    await customer_account_message_IK(callback_query.from_user.id)


