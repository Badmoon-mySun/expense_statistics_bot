import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from models.states import SignUp, Income, Expenses
from service.common import _is_url_ok
from models import add_to_db, check_db
from . import dp, bot


@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    """Обработка события команды /start"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text='Зарегестрироваться', callback_data='sign_up'),
        types.InlineKeyboardButton(text='Внести в таблицу', callback_data='add_to_table'),
    ]
    keyboard.add(*buttons)
    text = f"Я бот подчета финансовых расходов. Приятно познакомиться, {msg.from_user.first_name}.\n" \
           f"Вы можете:"
    await msg.answer(text=text, reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    """Обработка события команды /help"""
    await msg.answer(f'Я бот подчета финансовых расходов.')


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(msg: types.Message, state: FSMContext):
    """Разрешить пользователю отменять любое действие"""
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()


@dp.callback_query_handler(text='sign_up')
async def start_sing_up(msg: types.Message, state: FSMContext):
    """Запуск процесса регистрации"""
    if await check_db(f"SELECT telegram_id FROM customers WHERE telegram_id = {msg.from_user.id}") == False:
        text = "Введите Ваше имя:"
        await bot.send_message(msg.from_user.id, text=text)
        await SignUp.wait_for_name.set()
    else:
        await bot.send_message(msg.from_user.id, text='Пользователь уже существует!')
        await state.finish()


@dp.message_handler(state=SignUp.wait_for_name)
async def input_user_name(msg: types.Message, state: FSMContext):
    """Состояние 1: Ввод пользовательского имени"""
    if isinstance(msg.text, str):
        await state.update_data(user_name=msg.text)
    else:
        await bot.send_message(msg.from_user.id, text='Введите корректное имя')
    await SignUp.next()
    await msg.answer('Теперь введите сслыку на Ваш Google Sheets:')


@dp.message_handler(state=SignUp.wait_for_url)
async def input_sheets_url(msg: types.Message, state: FSMContext):
    """Состояние 2: Ввод URL-ссылки"""
    if msg.text.startswith('https://docs.google.com/spreadsheets/d/') and (await _is_url_ok(msg.text)):
        user_data = (msg.from_user.id, msg.text)
        await add_to_db('''INSERT INTO customers (telegram_id, sheet_url) VALUES (?, ?)''', user_data)

        await msg.answer("Регестрация завершена!")
        await state.finish()

    else:
        await bot.send_message(msg.from_user.id, text='Введите корректный URL')


@dp.callback_query_handler(text='add_to_table')
async def choose_operation(msg: types.Message, state: FSMContext):
    """Запуск процесса внесения операции"""
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("Доход", callback_data='Income'),
        types.InlineKeyboardButton("Расход", callback_data='Expenses'),
    ]
    keyboard.add(*buttons)
    await bot.send_message(msg.from_user.id, "Выберите операцию:", reply_markup=keyboard)

@dp.callback_query_handler(text='Income')
async def add_income_to_table(msg: types.Message, state: FSMContext):
    """Состояние 1: Ввод названия Дохода"""
    await bot.send_message(msg.from_user.id, "Введите название Дохода:")
    await Income.wait_for_income_name.set()

@dp.message_handler(state=Income.wait_for_income_name)
async def set_income_name(msg: types.Message, state: FSMContext):
    """Состояние 2: Ввод суммы Дохода"""
    if isinstance(msg.text, str):
        await state.update_data(income_name=msg.text)
        await msg.answer('Введите сумму Дохода:')
        await Income.next()
    else:
        await msg.answer("Введите корректную информацию")

@dp.message_handler(state=Income.wait_for_income_value)
async def set_income_value(msg: types.Message, state: FSMContext):
    """Добваление Дохода в Таблицу"""
    try:
        int(msg.text)
        store = await state.get_data()
        await msg.answer(f"Название: {store['income_name']}\nСумма: {msg.text}")

        # Операции с таблицей

        await msg.answer('Доход добавлен!')
        await state.finish()
    except:
        await msg.answer("Ошибка, повторите")


@dp.callback_query_handler(text='Expenses')
async def add_expense_to_table(msg: types.Message, state: FSMContext):
    """Состояние 1: Ввод названия Расхода"""
    await bot.send_message(msg.from_user.id, "Введите название Расхода:")
    await Expenses.wait_for_expenses_name.set()


@dp.message_handler(state=Expenses.wait_for_expenses_name)
async def set_expense_name(msg: types.Message, state: FSMContext):
    """Состояние 2: Ввод суммы Расхода"""
    if isinstance(msg.text, str):
        await state.update_data(expense_name=msg.text)
        await msg.answer('Введите сумму Расхода:')
        await Expenses.next()
    else:
        await msg.answer("Введите корректную информацию")

@dp.message_handler(state=Expenses.wait_for_expenses_value)
async def set_expense_value(msg: types.Message, state: FSMContext):
    """Добваление Расхода в Таблицу"""
    try:
        int(msg.text)
        store = await state.get_data()
        await msg.answer(f"Название: {store['expense_name']}\nСумма: {msg.text}")

        # Операции с таблицей

        await msg.answer('Расход добавлен!')
        await state.finish()
    except:
        await msg.answer("Ошибка, повторите")