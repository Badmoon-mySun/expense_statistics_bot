import logging
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

PROJECT_NAME = os.environ.get("PROJECT_NAME")
WEBAPP_HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT"))

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = "/webhook/" + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

DATABASE_NAME = 'sqlite.db'




