from sqlalchemy import Column, Integer, String

from bot import Base


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    sheet_url = Column(String, nullable=False)


