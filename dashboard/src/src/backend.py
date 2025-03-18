# src/backend.py

from src.alpha_vantage_api import fetch_intraday_data, fetch_daily_data

def get_intraday_features(symbol="IBM", interval="5min"):
    """Retrieves and processes intraday stock features."""
    data = fetch_intraday_data(symbol, interval)
    time_series_key = f"Time Series ({interval})"

    if time_series_key not in data:
        return None  # Handle API errors

    return [
        {
            "timestamp": timestamp,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"],
        }
        for timestamp, values in data[time_series_key].items()
    ]

def get_daily_features(symbol="IBM"):
    """Retrieves and processes daily stock features."""
    data = fetch_daily_data(symbol)
    time_series_key = "Time Series (Daily)"

    if time_series_key not in data:
        return None 

    return [
        {
            "date": date,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"],
        }
        for date, values in data[time_series_key].items()
    ]
