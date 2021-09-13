import sqlite3
import aiosqlite

from bot import DATABASE_NAME

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                sheet_url TEXT);''')

async def add_to_db(query, values):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute(query, values)
        await db.commit()

async def check_db(query):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute(query) as cursor:
            if await cursor.fetchone() is None:
                return False
            return True
