# Day 39 – Flight Deals Finder (Capstone Part 1)

Goal
- Query Tequila (Kiwi) for the next 6 months and alert if prices beat your sheet’s thresholds.

Setup
- Create a Google Sheet (columns: id, city, iataCode, lowestPrice) and connect with Sheety.
- Copy .env.example to .env and fill keys.

Run
```bash
pip install -r requirements.txt
python main.py
```

How it works
- Reads destinations via Sheety.
- Fills missing IATA codes.
- Searches round trips (nights_in_dst_from/to).
- If price < lowestPrice, sends SMS via Twilio (or prints if Twilio not set).

Env keys
- TEQUILA_API_KEY, ORIGIN_IATA, CURRENCY
- SHEETY_PRICES_ENDPOINT, SHEETY_TOKEN
- TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, ALERT_TO (optional)

Notes
- Adjust sheet payload keys in data_manager if your Sheety root key isn’t “prices”.
- Falls back to 1 stopover if no direct flight is found.