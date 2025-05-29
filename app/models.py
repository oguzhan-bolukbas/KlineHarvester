from sqlalchemy import Column, Integer, Text, Numeric, TIMESTAMP, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Kline(Base):
    __tablename__ = "klines"
    id = Column(Integer, primary_key=True)
    symbol = Column(Text, nullable=False)
    interval = Column(Text, nullable=False)
    open_time = Column(TIMESTAMP(timezone=True), nullable=False)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(Numeric)
    close_time = Column(TIMESTAMP(timezone=True))
    quote_asset_volume = Column(Numeric)
    number_of_trades = Column(Integer)
    taker_buy_base_asset_volume = Column(Numeric)
    taker_buy_quote_asset_volume = Column(Numeric)
    __table_args__ = (UniqueConstraint('symbol', 'interval', 'open_time', name='_symbol_interval_opentime_uc'),)
