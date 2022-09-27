from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram_calendar import simple_cal_callback
from aiogram_calendar.dialog_calendar import calendar_callback as dialog_cal_callback

from core import dp
from keyboards.user.common.flight_route_kb import departure_date_calendar_message_IK, departure_date_cancel_message_IK, \
    order_comment_message_IK
from states.CustomerStates import CustomerStates


def reg_customer_order_handlers():
    dp.register_callback_query_handler(customer_set_departure_date_calendar, dialog_cal_callback.filter(),
                                       state=CustomerStates.set_departure_date)
    dp.register_callback_query_handler(cancel_departure_date, state=CustomerStates.set_departure_date)
    dp.register_message_handler(customer_set_order_comment, state=CustomerStates.set_order_comment)


@dp.callback_query_handler(simple_cal_callback.filter(), state=CustomerStates.set_departure_date)
async def customer_set_departure_date_calendar(callback_query: types.CallbackQuery, callback_data: dict,
                                               state: FSMContext):
    await departure_date_calendar_message_IK(callback_query, callback_data, state, 'customer')


@dp.message_handler(state=CustomerStates.set_departure_date)
async def cancel_departure_date(message: types.Message, state: FSMContext):
    await departure_date_cancel_message_IK(message, state)


@dp.message_handler(state=CustomerStates.set_order_comment)
async def customer_set_order_comment(message: types.Message, state: FSMContext):
    await order_comment_message_IK(message, state, 'customer')
