from aiogram.dispatcher.filters.state import StatesGroup, State


class ItemMgmtStates(StatesGroup):
    ADD = State()
    UPDATE = State()
    DELETE = State()

