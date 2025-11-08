# Day 32 - Automated Birthday Email Sender

This project sends personalized birthday emails to friends listed in a CSV file.

## Features
- Reads `birthdays.csv` with columns: `name,email,year,month,day`
- Checks if today matches any birthday
- Chooses a random template from `letter_templates/`
- Replaces `[NAME]` placeholder in template
- Sends email via SMTP or prints in dry-run mode
- Configurable via environment variables (PowerShell friendly)

## Setup
1. Duplicate `.env.example` to `.env` (optional) or set vars directly in PowerShell.
2. Provide valid email credentials for an account that allows SMTP.
3. Ensure less-secure app access or app-specific password if using providers like Gmail.

### Required Environment Variables
```
EMAIL_USER      # SMTP username (email address)
EMAIL_PASS      # SMTP password or app password
SMTP_SERVER     # e.g., smtp.gmail.com
SMTP_PORT       # e.g., 587
USE_TLS         # true/false
DRY_RUN         # true to avoid sending for testing
FROM_NAME       # Display name for From header
```

### Setting Variables in PowerShell (temporary for session)
```powershell
$env:EMAIL_USER="your_email@example.com"
$env:EMAIL_PASS="your_app_password"
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:USE_TLS="true"
$env:DRY_RUN="true"   # Set to false when ready to actually send
$env:FROM_NAME="Birthday Bot"
```

### Running
Dry run (prints what would be sent):
```powershell
python .\main.py
```
Real send (after setting `DRY_RUN` to false):
```powershell
python .\main.py
```

## Extending
- Add more templates to `letter_templates/`
- Add more people or columns (e.g., custom message) to `birthdays.csv`
- Log sends to a file for auditing

## Notes
This script is kept simple for learning: no retry logic, rate limiting, or HTML mail. For production use, add error handling and logging.
