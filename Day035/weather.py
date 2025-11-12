"""Weather data fetching utilities for Day 35 Weather Alert App.

Uses OpenWeatherMap 5 day / 3 hour forecast API.
"""
from __future__ import annotations

import os
import requests
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    val = os.getenv(key)
    return val if val not in (None, "") else default


def fetch_forecast(lat: float, lon: float, api_key: str, units: str = "metric") -> Optional[Dict[str, Any]]:
    """Fetch the 5-day forecast (3h steps). Returns raw JSON dict or None on failure."""
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}
    try:
        r = requests.get(FORECAST_URL, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"[WARN] Forecast fetch failed: {e}")
        return None


def simplify_forecast(data: Dict[str, Any], horizon_hours: int) -> List[Dict[str, Any]]:
    """Simplify the forecast list to a smaller structure within horizon_hours.

    Returns list of dicts: {time_utc, dt, temp, weather_main, weather_desc, pop, rain_mm, snow_mm}.
    pop = probability of precipitation (0-1) if available.
    rain_mm / snow_mm aggregated from 'rain' or 'snow' keys per period.
    """
    now = datetime.now(timezone.utc).timestamp()
    cutoff = now + horizon_hours * 3600
    simplified: List[Dict[str, Any]] = []

    for item in data.get("list", []):
        dt = item.get("dt", 0)
        if dt > cutoff:
            continue
        main = item.get("main", {})
        weather_arr = item.get("weather", [])
        weather_main = weather_arr[0]["main"] if weather_arr else "?"
        weather_desc = weather_arr[0]["description"] if weather_arr else "?"
        pop = item.get("pop", 0.0)
        rain_mm = (item.get("rain", {}) or {}).get("3h", 0.0)
        snow_mm = (item.get("snow", {}) or {}).get("3h", 0.0)
        simplified.append({
            "dt": dt,
            "time_utc": datetime.fromtimestamp(dt, tz=timezone.utc),
            "temp": main.get("temp"),
            "weather_main": weather_main,
            "weather_desc": weather_desc,
            "pop": pop,
            "rain_mm": rain_mm,
            "snow_mm": snow_mm,
        })
    return simplified


def will_precipitate_periods(periods: List[Dict[str, Any]], pop_threshold: float = 0.5, mm_threshold: float = 0.1) -> List[Dict[str, Any]]:
    """Return periods likely to see precipitation based on probability or accumulated mm."""
    hits = []
    for p in periods:
        if p["pop"] >= pop_threshold or p["rain_mm"] >= mm_threshold or p["snow_mm"] >= mm_threshold:
            hits.append(p)
    return hits


if __name__ == "__main__":
    # Simple manual test (requires env vars)
    api = get_env("WEATHER_API_KEY")
    lat = float(get_env("LAT", "0") or 0)
    lon = float(get_env("LNG", "0") or 0)
    if api and lat and lon:
        raw = fetch_forecast(lat, lon, api)
        if raw:
            periods = simplify_forecast(raw, 12)
            print(f"Got {len(periods)} forecast periods in next 12h")
            wet = will_precipitate_periods(periods)
            print(f"Periods with precip: {len(wet)}")
        else:
            print("No forecast data.")
    else:
        print("Set WEATHER_API_KEY, LAT, LNG to test.")
