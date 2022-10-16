from aiogram import types

from core import dispatcher
from bot.filters.callback_filters import customer_cb
from bot.keyboards.user.customer.customer_kb import customer_account_message_IK
from bot.utils.chat_mgmt import delete_previous_messages


def reg_contractor_handlers():
    dispatcher.register_callback_query_handler(customer_account, customer_cb.filter(section='account'), state='*')


@dispatcher.callback_query_handler(customer_cb.filter(section='account'), state='*')
async def customer_account(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await customer_account_message_IK(callback_query.from_user.id)


