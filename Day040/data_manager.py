import os
import requests

SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT", "")
SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT", "")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN", "")

class DataManager:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"} if SHEETY_TOKEN else {}

    def get_destinations(self):
        """Get destination list from prices sheet."""
        r = requests.get(SHEETY_PRICES_ENDPOINT, headers=self.headers, timeout=15)
        r.raise_for_status()
        key = list(r.json().keys())[0]
        return r.json()[key]

    def update_iata_codes(self, rows):
        """Update IATA codes in sheet."""
        for row in rows:
            rid = row["id"]
            body = {"price": {"iataCode": row["iataCode"]}}
            requests.put(
                f"{SHEETY_PRICES_ENDPOINT}/{rid}",
                json=body,
                headers=self.headers,
                timeout=15
            ).raise_for_status()
    
    def get_users(self):
        """Get registered users from users sheet."""
        if not SHEETY_USERS_ENDPOINT:
            return []
        
        r = requests.get(SHEETY_USERS_ENDPOINT, headers=self.headers, timeout=15)
        r.raise_for_status()
        key = list(r.json().keys())[0]  # e.g., "users"
        return r.json()[key]