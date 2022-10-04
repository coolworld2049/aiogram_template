from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    set_name = State()
    creating = State()
    accepted = State()
    progress = State()
    completed = State()
    terminated = State()
