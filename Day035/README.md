# Day 35 — Project Starter

This directory is set up and ready for your Day 35 project. Use `main.py` as the entry point and add any supporting modules or data files alongside it.

## Suggested structure
- `main.py` — program entry point
- `README.md` — this file; document what you build today
- `data/` (optional) — input files or assets
- `config/` (optional) — environment/config files

## Getting started
1. Open `main.py` and sketch the minimal program structure (functions/classes).
2. If your project talks to an API, prefer environment variables for secrets.
3. Add a quick note here about how to run your program.

## Environment variables (optional)
If you need API keys or credentials, set them per session in PowerShell:
```powershell
# Day 35 — Weather Alert App

Check the upcoming weather using OpenWeatherMap and notify you if precipitation is likely within a chosen time horizon.

## Features
- Uses OpenWeatherMap 5-day/3-hour forecast API
- Checks next N hours for likely precipitation
- Optional email notification (SMTP)
- Dry-run mode to preview messages without sending
- Force mode for testing
- Optional loop mode to run periodically

## Setup
1. Get a free API key from OpenWeatherMap: https://openweathermap.org/api
2. Set environment variables (PowerShell examples below) or copy `.env.example` values into your session.

### Environment Variables
```
WEATHER_API_KEY   # required
LAT               # required (decimal latitude)
LNG               # required (decimal longitude)
UNITS=metric      # metric or imperial

# Email (optional)
EMAIL_USER        # sender address
EMAIL_PASS        # password/app password
TO_EMAIL          # recipient (defaults to EMAIL_USER)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
USE_TLS=true
FROM_NAME="Weather Alert"

# Behavior
DRY_RUN=true
FORCE_ALERT=false
CHECK_INTERVAL=1800      # seconds (30m) for --loop
ALERT_HORIZON_HOURS=12   # forecast horizon
```

### PowerShell examples
```powershell
$env:WEATHER_API_KEY="your_api_key"
$env:LAT="40.7128"; $env:LNG="-74.0060"   # NYC
$env:UNITS="metric"

# Email (optional)
$env:EMAIL_USER="your_email@example.com"
$env:EMAIL_PASS="your_app_password"
$env:TO_EMAIL="your_email@example.com"
$env:USE_TLS="true"
$env:DRY_RUN="true"
$env:FROM_NAME="Weather Alert"
```

## Run
Single check:
```powershell
python .\main.py
```
Force + dry run (for testing):
```powershell
python .\main.py --force --dry-run
```
Loop (every CHECK_INTERVAL seconds):
```powershell
python .\main.py --loop
```

## How it works
- Fetches forecast with `lat`, `lon`, `appid`, and `units`.
- Simplifies the next `ALERT_HORIZON_HOURS` of 3-hour periods.
- Flags an alert if any period has:
	- probability of precipitation (pop) >= 0.5, or
	- rain/snow accumulation >= 0.1mm for that 3-hour window.
- Sends an email or prints the message in dry-run mode.

## Notes
- Ensure your email provider allows SMTP (you may need an app password).
- OpenWeatherMap free tier may rate-limit; consider caching if looping frequently.
- You can adjust thresholds in `weather.py` if you want stricter/looser alerts.
