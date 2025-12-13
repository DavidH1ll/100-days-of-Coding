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