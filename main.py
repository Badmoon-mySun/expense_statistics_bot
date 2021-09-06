import os
import logging
import aiohttp

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import SignUp

load_dotenv(find_dotenv())

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

# async def _is_url_ok(url):
#     try:
#        async with aiohttp.ClientSession() as session:
#            async with session.get(url) as resp:
#                return resp.status == 200
#     except:
#         return False

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
async def save_user_name(message: types.Message, state: FSMContext):
    """Состояние 1: Ввод пользовательского имени"""
    if isinstance(message.text, str):
        await state.update_data(user_name=message.text)
    await SignUp.next()
    await message.answer('Теперь введите сслыку на Ваш Google Sheets:')


@dp.message_handler(state=SignUp.wait_for_url)
async def save_url(message: types.Message, state: FSMContext):
    """Состояние 2: Ввод URL-ссылки"""
    if 'https://docs.google.com/spreadsheets/' in message.text:
        # print(await _is_url_ok(message.text))
        store = await state.get_data()
        await message.answer(f"Ваше имя - {store['user_name']}\n"
                             f"Ваш URL - {message.text}")
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, text='Выход')


if __name__ == '__main__':
    executor.start_polling(dp)
