import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


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


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    print(msg.from_user.id)  # 732843764
    if msg.text.lower() == 'привет':
        await msg.answer('Привет!')
    else:
        await msg.answer('Не понимаю, что это значит.')


if __name__ == '__main__':
    executor.start_polling(dp)
