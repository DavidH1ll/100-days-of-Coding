import os
import requests

TEQUILA_BASE = "https://api.tequila.kiwi.com"
TEQUILA_KEY = os.getenv("TEQUILA_API_KEY", "")

class FlightSearch:
    def __init__(self, currency: str = "GBP"):
        self.currency = currency
        self.headers = {"apikey": TEQUILA_KEY}

    def get_iata_code(self, city: str) -> str:
        r = requests.get(
            f"{TEQUILA_BASE}/locations/query",
            headers=self.headers,
            params={"term": city, "location_types": "city"},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json().get("locations", [])
        return data[0]["code"] if data else ""

    def search_round_trip(
        self,
        fly_from: str,
        fly_to: str,
        date_from: str,
        date_to: str,
        nights_min: int = 5,
        nights_max: int = 21,
        max_stopovers: int = 0,
    ):
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": nights_min,
            "nights_in_dst_to": nights_max,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": self.currency,
            "max_stopovers": max_stopovers,
        }
        r = requests.get(f"{TEQUILA_BASE}/v2/search", headers=self.headers, params=params, timeout=25)
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data:
            return None
        best = data[0]
        return {
            "price": best["price"],
            "cityFrom": best["cityFrom"],
            "cityTo": best["cityTo"],
            "flyFrom": best["flyFrom"],
            "flyTo": best["flyTo"],
            "out_date": best["route"][0]["local_departure"].split("T")[0],
            "return_date": best["route"][-1]["local_departure"].split("T")[0],
            "link": best.get("deep_link") or "https://www.google.com/travel/flights",
        }