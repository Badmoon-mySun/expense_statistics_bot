from sqlalchemy import create_engine, Column, DateTime, ForeignKey,\
Numeric, CheckConstraint, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Подключение к БД SQLite
engine = create_engine('sqlite:///sqlite3.db')
conn = engine.connect()

# Декларированный класс
Base = declarative_base()

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    sheet_url = Column(String, nullable=False)


