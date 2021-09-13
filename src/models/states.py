from aiogram.dispatcher.filters.state import State, StatesGroup


class SignUp(StatesGroup):
    """Инициализацния состояний"""
    wait_for_name = State()
    wait_for_url = State()
