import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from fetcher import get_klines
from models import Base
from crud import insert_klines
import time
import json
import concurrent.futures
import logging

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "klines")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


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
    return all_klines


def fetch_klines_in_range(symbol, interval, start_date, end_date):
    """
    Fetch klines for a symbol and interval between two datetime.date or datetime.datetime objects (inclusive).
    Dates should be in UTC.
    """
    start_time = int(datetime.combine(start_date, datetime.min.time()).timestamp() * 1000)
    end_time = int(datetime.combine(end_date, datetime.max.time()).timestamp() * 1000)
    all_klines = []
    while True:
        klines = get_klines(symbol, interval, start_time=start_time, end_time=end_time, limit=1000)
        if not klines:
            break
        all_klines += klines
        last_close_time = klines[-1][6]
        # If less than 1000 or last kline's close_time >= end_time, stop
        if len(klines) < 1000 or last_close_time >= end_time:
            break
        # Move start_time forward to avoid overlap
        start_time = last_close_time + 1
    return all_klines


def fetch_and_insert(symbol, interval):
    session = SessionLocal()
    try:
        logging.info(f"Fetching {symbol} {interval}...")
        # klines = fetch_all_klines(symbol, interval)
        start_date = date(2024, 1, 1)
        end_date = date(2025, 5, 31)
        klines = fetch_klines_in_range(symbol, interval, start_date, end_date)
        logging.info(f"Fetched {len(klines)} klines for {symbol} in {interval}. Inserting into DB...")
        insert_klines(session, symbol, interval, klines)
        logging.info(f"Done: {symbol} {interval}")
    finally:
        session.close()


def main():
    Base.metadata.create_all(bind=engine)
    symbols = read_symbols("symbols.json")
    intervals = read_intervals("intervals.json")
    max_workers = 16  # Start with 16 threads, decrease if errors occur
    logging.info(f"Using max_workers={max_workers}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for symbol in symbols:
            for interval in intervals:
                futures.append(executor.submit(fetch_and_insert, symbol, interval))
            time.sleep(120)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                logging.error(f"Thread generated an exception: {exc}")
    logging.info(f"\n\n***** ALL THREADS COMPLETED! *****\n")

if __name__ == "__main__":
    main()
