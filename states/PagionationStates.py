from aiogram.dispatcher.filters.state import StatesGroup, State


class PaginationStates(StatesGroup):
    step = State()
