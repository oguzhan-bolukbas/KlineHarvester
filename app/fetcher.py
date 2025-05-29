import requests
import os
from datetime import datetime

def get_klines(symbol, interval, start_time=None, end_time=None, limit=1000):
    base_url = os.getenv("BINANCE_API_BASE", "https://api.binance.com")
    endpoint = f"/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    if start_time:
        params["startTime"] = int(start_time)
    if end_time:
        params["endTime"] = int(end_time)
    url = base_url + endpoint
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
