"""
Day 40: Flight Club - User Sign-up & Email Notifications (Capstone Part 2)
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from customer_acquisition import CustomerAcquisition
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

ORIGIN_IATA = os.getenv("ORIGIN_IATA", "LON")
CURRENCY = os.getenv("CURRENCY", "GBP")
NIGHTS_MIN = int(os.getenv("NIGHTS_MIN", "5"))
NIGHTS_MAX = int(os.getenv("NIGHTS_MAX", "21"))


def check_configuration() -> bool:
    """Validate required environment variables."""
    required = {
        "TEQUILA_API_KEY": "Tequila flight search API key",
        "SHEETY_PRICES_ENDPOINT": "Google Sheets prices endpoint"
    }
    
    missing = []
    for var, desc in required.items():
        if not os.getenv(var):
            missing.append(f"  ❌ {var} ({desc})")
    
    if missing:
        print("\n⚠️  Missing required environment variables:")
        for m in missing:
            print(m)
        print("\n📝 Create a .env file in Day040 folder with:")
        print("   TEQUILA_API_KEY=your_key")
        print("   SHEETY_PRICES_ENDPOINT=https://api.sheety.co/xxx/flightDeals/prices")
        print("\n💡 Copy .env.example to .env and fill in your values.\n")
        return False
    
    return True


def find_cheap_flights() -> List[Dict]:
    """Search for flights cheaper than threshold prices."""
    dm = DataManager()
    fs = FlightSearch(currency=CURRENCY)
    
    destinations = dm.get_destinations()
    
    # Backfill IATA codes if missing
    updated = False
    for row in destinations:
        if not row.get("iataCode"):
            row["iataCode"] = fs.get_iata_code(row["city"])
            updated = True
    
    if updated:
        dm.update_iata_codes(destinations)
    
    # Search for deals
    date_from = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    date_to = (datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")
    
    deals = []
    
    for dest in destinations:
        target_price = float(dest["lowestPrice"])
        dest_iata = dest["iataCode"]
        
        if not dest_iata:
            continue
        
        # Try direct flight
        result = fs.search_round_trip(
            fly_from=ORIGIN_IATA,
            fly_to=dest_iata,
            date_from=date_from,
            date_to=date_to,
            nights_min=NIGHTS_MIN,
            nights_max=NIGHTS_MAX,
            max_stopovers=0,
        )
        
        # Try with 1 stopover if no direct
        if not result:
            result = fs.search_round_trip(
                fly_from=ORIGIN_IATA,
                fly_to=dest_iata,
                date_from=date_from,
                date_to=date_to,
                nights_min=NIGHTS_MIN,
                nights_max=NIGHTS_MAX,
                max_stopovers=1,
            )
        
        if result and result["price"] < target_price:
            deals.append({
                "city": dest["city"],
                "price": result["price"],
                "origin": f"{result['cityFrom']} ({result['flyFrom']})",
                "destination": f"{result['cityTo']} ({result['flyTo']})",
                "out_date": result["out_date"],
                "return_date": result["return_date"],
                "link": result["link"],
                "savings": target_price - result["price"]
            })
            print(f"✓ Found deal: {dest['city']} for {CURRENCY}{result['price']} (saves {CURRENCY}{target_price - result['price']})")
    
    return deals


def notify_users(deals: List[Dict]):
    """Send email notifications to all registered users."""
    if not deals:
        print("No deals found today.")
        return
    
    dm = DataManager()
    users = dm.get_users()
    
    if not users:
        print("No users registered yet.")
        return
    
    notifier = NotificationManager()
    
    # Format email body
    email_body = "🎉 Flight Club - Today's Best Deals!\n\n"
    email_body += f"We found {len(deals)} amazing flight deal(s) for you:\n\n"
    
    for i, deal in enumerate(deals, 1):
        email_body += f"{i}. {deal['city']}\n"
        email_body += f"   Price: {CURRENCY}{deal['price']} (save {CURRENCY}{deal['savings']}!)\n"
        email_body += f"   Route: {deal['origin']} → {deal['destination']}\n"
        email_body += f"   Dates: {deal['out_date']} to {deal['return_date']}\n"
        email_body += f"   Book: {deal['link']}\n\n"
    
    email_body += "\nHappy travels! ✈️\n- Flight Club Team"
    
    # Send to all users
    for user in users:
        email = user.get("email")
        first_name = user.get("firstName", "Traveler")
        
        if email:
            personalized_body = f"Hi {first_name},\n\n{email_body}"
            notifier.send_email(
                to_email=email,
                subject=f"Flight Club Alert: {len(deals)} Cheap Flight(s) Found!",
                body=personalized_body
            )
            print(f"✓ Sent email to {first_name} ({email})")


def main():
    """Main CLI."""
    if not check_configuration():
        sys.exit(1)
    
    print("=" * 60)
    print("✈️  FLIGHT CLUB - Your Personal Flight Deal Hunter")
    print("=" * 60)
    print("\nWhat would you like to do?")
    print("1. Register new users")
    print("2. Search for flight deals and notify users")
    print("3. Exit")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\n--- User Registration ---")
        ca = CustomerAcquisition()
        ca.register_users()
    
    elif choice == "2":
        print("\n--- Searching for Flight Deals ---")
        deals = find_cheap_flights()
        
        if deals:
            print(f"\n✅ Found {len(deals)} deal(s)!")
            notify_users(deals)
        else:
            print("\n❌ No deals found cheaper than thresholds.")
    
    elif choice == "3":
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid choice.")


if __name__ == "__main__":
    main()
