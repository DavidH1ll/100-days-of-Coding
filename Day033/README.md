# Day 33 - ISS Overhead Email Notifier

Track the International Space Station (ISS) and get an email when it's overhead at night.

## Overview
This script periodically:
1. Fetches current ISS latitude/longitude from `http://api.open-notify.org/iss-now.json`.
2. Fetches today's sunrise and sunset times for your location via `https://api.sunrise-sunset.org/json`.
3. Determines if it's currently nighttime.
4. Calculates an approximate angular distance between you and the ISS. If within threshold and night, sends (or prints) an email notification.

## Environment Variables
Copy `.env.example` and set values or assign in PowerShell. Key vars:
```
LAT                  # Your latitude (decimal degrees)
LNG                  # Your longitude
EMAIL_USER           # SMTP username (sender address)
EMAIL_PASS           # SMTP password/app password
TO_EMAIL             # Recipient (defaults to EMAIL_USER if empty)
SMTP_SERVER          # SMTP host
SMTP_PORT            # SMTP port
USE_TLS              # true/false
DRY_RUN              # Print message instead of sending
FROM_NAME            # Display name in From header
FORCE_NOTIFY         # true to always send/print (testing)
CHECK_INTERVAL       # Seconds between loop iterations
DISTANCE_DEG_THRESHOLD # Degrees threshold for overhead (default 5)
```

### PowerShell Example
```powershell
$env:LAT="40.7128"
$env:LNG="-74.0060"
$env:EMAIL_USER="your_email@example.com"
$env:EMAIL_PASS="your_app_password"
$env:TO_EMAIL="your_email@example.com"
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:USE_TLS="true"
$env:DRY_RUN="true"
$env:FROM_NAME="ISS Notifier"
$env:FORCE_NOTIFY="false"
$env:CHECK_INTERVAL="600"
$env:DISTANCE_DEG_THRESHOLD="5"
```

## Run Once (manual check)
```powershell
python .\main.py
```

## Continuous Loop
Add `--loop` flag:
```powershell
python .\main.py --loop
```
Stops with Ctrl + C.

## Testing
Set `FORCE_NOTIFY=true` and `DRY_RUN=true` to verify email formatting regardless of position or night:
```powershell
$env:FORCE_NOTIFY="true"; $env:DRY_RUN="true"; python .\main.py
```

## Notes
- This is a learning exercise: distance calc is rough (simple spherical law of cosines).
- Night definition uses sunrise-sunset API (sunset to next sunrise).
- Add error handling/backoffs for production use.
