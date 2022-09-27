from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderStates(StatesGroup):
    order_start_creating = State()
    order_accepted = State()
    order_in_work = State()
    order_completed = State()
    order_terminated = State()
    order_customer_deleted = State()
