from aiogram.dispatcher.filters.state import State, StatesGroup


class SignUp(StatesGroup):
    """Инициализацния состояний для регестации пользователя"""
    wait_for_name = State()
    wait_for_url = State()

class Income(StatesGroup):
    """Инициализация состояний для ввода доходов"""
    wait_for_income_name = State()
    wait_for_income_value = State()

class Expenses(StatesGroup):
    """Инициализация состояний для ввода расходов"""
    wait_for_expenses_name = State()
    wait_for_expenses_value = State()


