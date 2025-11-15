"""Stock data fetching module using Alpha Vantage API.

Retrieves daily stock prices and calculates percentage changes.
"""
from __future__ import annotations

import os
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple


ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


def fetch_daily_prices(symbol: str, api_key: str) -> Optional[Dict[str, Dict[str, float]]]:
    """Fetch daily time series data for a stock symbol.
    
    Returns dict with dates as keys and OHLC data as values, or None on failure.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact"  # last 100 data points
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            print(f"[ERROR] Alpha Vantage: {data['Error Message']}")
            return None
        
        if "Note" in data:
            print(f"[WARN] Alpha Vantage: {data['Note']}")  # Rate limit warning
            return None
        
        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            print("[ERROR] No time series data returned")
            return None
        
        # Convert string values to floats
        result = {}
        for date_str, values in time_series.items():
            result[date_str] = {
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": float(values["5. volume"])
            }
        
        return result
    
    except requests.RequestException as e:
        print(f"[ERROR] Stock API request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Failed to parse stock data: {e}")
        return None


def get_last_two_closes(daily_data: Dict[str, Dict[str, float]]) -> Optional[Tuple[float, float, str, str]]:
    """Extract the last two closing prices from daily data.
    
    Returns (yesterday_close, day_before_close, yesterday_date, day_before_date) or None.
    """
    if not daily_data or len(daily_data) < 2:
        return None
    
    # Sort dates descending
    sorted_dates = sorted(daily_data.keys(), reverse=True)
    
    yesterday = sorted_dates[0]
    day_before = sorted_dates[1]
    
    yesterday_close = daily_data[yesterday]["close"]
    day_before_close = daily_data[day_before]["close"]
    
    return yesterday_close, day_before_close, yesterday, day_before


def calculate_percent_change(current: float, previous: float) -> float:
    """Calculate percentage change between two prices."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def get_stock_change(symbol: str, api_key: str) -> Optional[Dict[str, any]]:
    """Get stock price change information.
    
    Returns dict with: symbol, yesterday_close, day_before_close, change_percent,
    direction (UP/DOWN), yesterday_date, day_before_date
    """
    daily_data = fetch_daily_prices(symbol, api_key)
    if not daily_data:
        return None
    
    result = get_last_two_closes(daily_data)
    if not result:
        print("[ERROR] Not enough historical data")
        return None
    
    yesterday_close, day_before_close, yesterday_date, day_before_date = result
    
    change_percent = calculate_percent_change(yesterday_close, day_before_close)
    direction = "🔺" if change_percent > 0 else "🔻"
    
    return {
        "symbol": symbol,
        "yesterday_close": yesterday_close,
        "day_before_close": day_before_close,
        "yesterday_date": yesterday_date,
        "day_before_date": day_before_date,
        "change_percent": change_percent,
        "direction": direction,
        "abs_change_percent": abs(change_percent)
    }


if __name__ == "__main__":
    # Test
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if api_key:
        change = get_stock_change("TSLA", api_key)
        if change:
            print(f"{change['symbol']}: {change['direction']} {change['abs_change_percent']:.2f}%")
            print(f"  {change['day_before_date']}: ${change['day_before_close']:.2f}")
            print(f"  {change['yesterday_date']}: ${change['yesterday_close']:.2f}")
    else:
        print("Set ALPHA_VANTAGE_API_KEY to test")
