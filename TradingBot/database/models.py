from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, Sequence
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

transaction_types = (("BUY", "BUY"), ("SELL", "SELL"))


class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, Sequence("order_seq"), primary_key=True)
    client_id = Column(String(50))
    coinbase_id = Column(String(50))
    transaction_type = Column(String(10))
    product = Column(String(10))
    price = Column(String(10))
    base_currency_balance_before_order = Column(String(10))
    quote_currency_balance_before_order = Column(String(10))
    base_currency_balance_after_order = Column(String(10))
    quote_currency_balance_after_order = Column(String(10))
    time_of_order = Column(DateTime)
    additional_info = Column(Text, nullable=True)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_onupdate=func.now())

    def __repr__(self):
        return str(self.__dict__)
