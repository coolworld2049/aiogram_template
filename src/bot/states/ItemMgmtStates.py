from aiogram.dispatcher.filters.state import StatesGroup, State


class ItemMgmtStates(StatesGroup):
    PICK = State()
    ADD = State()
    UPDATE = State()
    DELETE = State()

