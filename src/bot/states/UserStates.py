from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    SET_NAME = State()
    CREATED = State()
    ACCEPTED = State()
    PROGRESS = State()
    COMPLETED = State()
    TERMINATED = State()
