import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from fetcher import get_klines
from models import Base
from crud import insert_klines
import time
import json

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "klines")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Read symbols and intervals from file
def read_symbols(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def read_intervals(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def fetch_all_klines(symbol, interval):
    # Binance max 1000 per request, fetch backwards
    end_time = int(datetime.now().timestamp() * 1000)
    all_klines = []
    while True:
        klines = get_klines(symbol, interval, end_time=end_time, limit=1000)
        if not klines:
            break
        all_klines = klines + all_klines
        first_open_time = klines[0][0]
        if len(klines) < 1000:
            break
        end_time = first_open_time - 1
        time.sleep(0.5)  # avoid rate limits
    return all_klines

def main():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    symbols = read_symbols("symbols.json")
    intervals = read_intervals("intervals.json")
    for symbol in symbols:
        for interval in intervals:
            print(f"Fetching {symbol} {interval}...")
            klines = fetch_all_klines(symbol, interval)
            print(f"Fetched {len(klines)} klines. Inserting into DB...")
            insert_klines(session, symbol, interval, klines)
            print(f"Done: {symbol} {interval}")
    session.close()

if __name__ == "__main__":
    main()
