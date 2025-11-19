"""
Customer acquisition module - handles user sign-up and validation.
"""

import os
import re
import requests
from typing import Dict, Optional

SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT", "")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN", "")


class CustomerAcquisition:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"} if SHEETY_TOKEN else {}
    
    def validate_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_name(self, name: str) -> bool:
        """Validate name (letters, spaces, hyphens only)."""
        pattern = r'^[a-zA-Z\s\-]+$'
        return len(name) >= 2 and re.match(pattern, name) is not None
    
    def add_user(self, first_name: str, last_name: str, email: str) -> bool:
        """Add user to Google Sheets via Sheety."""
        if not SHEETY_USERS_ENDPOINT:
            print("❌ SHEETY_USERS_ENDPOINT not configured.")
            return False
        
        # Sheety payload format (adjust key if sheet name differs)
        body = {
            "user": {
                "firstName": first_name.title(),
                "lastName": last_name.title(),
                "email": email.lower()
            }
        }
        
        try:
            response = requests.post(
                SHEETY_USERS_ENDPOINT,
                json=body,
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            print(f"✅ Successfully added {first_name} {last_name} to Flight Club!")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to add user: {e}")
            return False
    
    def register_users(self):
        """Interactive CLI for registering multiple users."""
        print("\n🎯 Welcome to Flight Club!")
        print("Get daily emails with the cheapest flight deals.\n")
        
        while True:
            print("-" * 60)
            
            # Get first name
            while True:
                first_name = input("First Name: ").strip()
                if self.validate_name(first_name):
                    break
                print("❌ Invalid name. Use letters, spaces, or hyphens only.")
            
            # Get last name
            while True:
                last_name = input("Last Name: ").strip()
                if self.validate_name(last_name):
                    break
                print("❌ Invalid name. Use letters, spaces, or hyphens only.")
            
            # Get email with confirmation
            while True:
                email = input("Email: ").strip()
                if not self.validate_email(email):
                    print("❌ Invalid email format. Try again.")
                    continue
                
                email_confirm = input("Confirm Email: ").strip()
                if email.lower() == email_confirm.lower():
                    break
                print("❌ Emails don't match. Try again.")
            
            # Add to sheet
            self.add_user(first_name, last_name, email)
            
            # Ask if more users
            more = input("\nRegister another user? (y/n): ").strip().lower()
            if more != 'y':
                print("\n✅ Registration complete!")
                break

from datetime import datetime, timedelta
import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

ORIGIN_IATA = os.getenv("ORIGIN_IATA", "LON")  # e.g., LON, DUB, JFK
CURRENCY = os.getenv("CURRENCY", "GBP")

def date_range_months(months: int = 6):
    start = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    end = (datetime.now() + timedelta(days=30 * months)).strftime("%d/%m/%Y")
    return start, end

def main():
    dm = DataManager()
    fs = FlightSearch(currency=CURRENCY)
    notifier = NotificationManager()

    # 1) Load destinations (Google Sheet via Sheety)
    destinations = dm.get_destinations()  # [{id, city, iataCode, lowestPrice}, ...]

    # 2) Backfill IATA codes if missing
    updated = False
    for row in destinations:
        if not row.get("iataCode"):
            row["iataCode"] = fs.get_iata_code(row["city"])
            updated = True
    if updated:
        dm.update_iata_codes(destinations)

    # 3) Search flights next 6 months
    date_from, date_to = date_range_months(6)
    for row in destinations:
        target_price = float(row["lowestPrice"])
        dest_iata = row["iataCode"]
        result = fs.search_round_trip(
            fly_from=ORIGIN_IATA,
            fly_to=dest_iata,
            date_from=date_from,
            date_to=date_to,
            nights_min=int(os.getenv("NIGHTS_MIN", "5")),
            nights_max=int(os.getenv("NIGHTS_MAX", "21")),
            max_stopovers=0,
        )

        if not result:
            # Optional: try with one stopover
            result = fs.search_round_trip(
                fly_from=ORIGIN_IATA,
                fly_to=dest_iata,
                date_from=date_from,
                date_to=date_to,
                nights_min=int(os.getenv("NIGHTS_MIN", "5")),
                nights_max=int(os.getenv("NIGHTS_MAX", "21")),
                max_stopovers=1,
            )

        if not result:
            print(f"No flight found for {row['city']}.")
            continue

        price = result["price"]
        if price < target_price:
            msg = (
                f"Low price alert! Only {CURRENCY} {price} to fly "
                f"{result['cityFrom']} ({result['flyFrom']}) → {result['cityTo']} ({result['flyTo']}), "
                f"{result['out_date']} to {result['return_date']}. {result['link']}"
            )
            print(msg)
            notifier.send(msg)
        else:
            print(f"{row['city']}: found {CURRENCY} {price} (threshold {target_price}).")

if __name__ == "__main__":
    main()