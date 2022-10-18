from aiogram import types

from core import dispatcher
from bot.filters.callback_filters import contractor_cb
from bot.keyboards.user.contractor.contractor_kb import contractor_account_message_IK
from helpers.bot.chat_mgmt import delete_previous_messages


def reg_customer_handlers():
    dispatcher.register_callback_query_handler(contractor_account, contractor_cb.filter(section='account'), state='*')


@dispatcher.callback_query_handler(contractor_cb.filter(section='account'), state='*')
async def contractor_account(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    await contractor_account_message_IK(callback_query.from_user.id)
