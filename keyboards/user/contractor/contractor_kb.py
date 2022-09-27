from aiogram import types

from core import bot
from config import MESSAGE_DELAY
from data.database.database import fetchone, fetchmany
from keyboards.user.customer.customer_kb import formate_order_status
from states.OrderStates import OrderStates
from utils.chat_mgmt import delete_message, save_message, get_last_message


async def contractor_account_message_IK(user_id: int):
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    pass
