import os

import logging

from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from common import _is_url_ok
from aiogram import types

from states import SignUp
from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv, find_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv(find_dotenv())

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)


PROJECT_NAME=os.environ.get("PROJECT_NAME")
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT"))

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = "/webhook/" + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


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
async def cancel_handler(message: types.Message, state: FSMContext):
    """Разрешить пользователю отменять любое действие"""
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()


@dp.callback_query_handler(text='sign_up')
async def start_sing_up(message: types.Message, state: FSMContext):
    """Запуск процесса регистрации"""
    text = "Введите Ваше имя:"
    await bot.send_message(message.from_user.id, text=text)
    await SignUp.wait_for_name.set()


@dp.message_handler(state=SignUp.wait_for_name)
async def input_user_name(message: types.Message, state: FSMContext):
    """Состояние 1: Ввод пользовательского имени"""
    if isinstance(message.text, str):
        await state.update_data(user_name=message.text)
    else:
        await bot.send_message(message.from_user.id, text='Введите корректное имя')
    await SignUp.next()
    await message.answer('Теперь введите сслыку на Ваш Google Sheets:')


@dp.message_handler(state=SignUp.wait_for_url)
async def input_sheets_url(message: types.Message, state: FSMContext):
    """Состояние 2: Ввод URL-ссылки"""
    if message.text.startswith('https://docs.google.com/spreadsheets/d/') and (await _is_url_ok(message.text)):
        store = await state.get_data()
        await message.answer(f"Ваше имя - {store['user_name']}\n"
                             f"Ваш URL - {message.text}")
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, text='Введите корректный URL')


# Run after startup
async def on_startup(dispatcher: Dispatcher) -> None:
    logging.info('Starting connection.')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    logging.info('Connection success.')


# Run before shutdown
async def on_shutdown(dispatcher: Dispatcher) -> None:
    logging.info("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Bot down")


if __name__ == "__main__":
    logging.info(WEBAPP_HOST)
    logging.info(WEBAPP_PORT)
    logging.info(PROJECT_NAME)

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
