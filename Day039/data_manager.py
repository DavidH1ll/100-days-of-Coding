import os
import requests

SHEETY_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT", "")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN", "")

class DataManager:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"} if SHEETY_TOKEN else {}

    def get_destinations(self):
        r = requests.get(SHEETY_ENDPOINT, headers=self.headers, timeout=15)
        r.raise_for_status()
        # Expecting payload like {"prices":[{id,city,iataCode,lowestPrice}, ...]}
        key = list(r.json().keys())[0]  # e.g., "prices"
        return r.json()[key]

    def update_iata_codes(self, rows):
        # PUT each row back with updated iataCode
        for row in rows:
            rid = row["id"]
            body = {"price": {"iataCode": row["iataCode"]}}  # adjust key if your sheet name differs
            requests.put(f"{SHEETY_ENDPOINT}/{rid}", json=body, headers=self.headers, timeout=15).raise_for_status()