from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    set_name = State()
    set_phone = State()
    set_photo = State()
