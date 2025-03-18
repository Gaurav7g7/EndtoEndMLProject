# src/alpha_vantage_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

BASE_URL = "https://www.alphavantage.co/query"

def fetch_intraday_data(symbol="IBM", interval="5min", outputsize="compact"):
    """Fetch intraday stock data from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def fetch_daily_data(symbol="IBM", outputsize="compact"):
    """Fetch daily stock data from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()
