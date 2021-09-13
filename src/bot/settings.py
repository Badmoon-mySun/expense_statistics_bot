import logging
import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(find_dotenv())

TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

PROJECT_NAME = os.environ.get("PROJECT_NAME")
WEBAPP_HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT"))

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = "/webhook/" + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Подключение к БД SQLite
engine = create_engine('sqlite:///sqlite3.db')
conn = engine.connect()

# Декларированный класс
Base = declarative_base()
