from aiogram import types

from core import dp
from filters.callback_filters import contractor_cb
from keyboards.user.contractor.contractor_kb import contractor_account_message_IK
from utils.chat_mgmt import delete_previous_messages


def reg_customer_handlers():
    dp.register_callback_query_handler(contractor_account, contractor_cb.filter(section='account'), state='*')


@dp.callback_query_handler(contractor_cb.filter(section='account'), state='*')
async def contractor_account(callback_query: types.CallbackQuery):
    msg_ids = callback_query.data.split('_')[-1]
    await delete_previous_messages(msg_ids=msg_ids, tgtype=callback_query)
    await contractor_account_message_IK(callback_query.from_user.id)
