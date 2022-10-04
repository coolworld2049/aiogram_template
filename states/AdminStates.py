from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    add_item = State()
    update_item = State()
    delete_item = State()

