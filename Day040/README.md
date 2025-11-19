# Day 40 – Flight Club Product (Capstone Part 2)

## Goal
Upgrade Day 39's personal flight tracker into a **full product** with:
- ✅ User registration system
- ✅ Email validation
- ✅ Google Sheets user management
- ✅ Mass email notifications to all users
- ✅ Professional email formatting

## New Features

### User Registration
- CLI-based sign-up flow
- Email validation with regex
- Name validation (letters, spaces, hyphens)
- Email confirmation (type twice)
- Stored in Google Sheets "users" tab

### Email Notifications
- SMTP integration (Gmail, Outlook, etc.)
- Personalized emails with user's first name
- Formatted deal summaries
- Multiple deals in single email
- Professional email template

## Setup

### 1. Google Sheets Structure

**Sheet 1: prices** (same as Day 39)
| id | city | iataCode | lowestPrice |
|----|------|----------|-------------|
| 1  | Paris | CDG | 50 |

**Sheet 2: users** (new for Day 40)
| id | firstName | lastName | email |
|----|-----------|----------|-------|
| 1  | John | Doe | john@example.com |

### 2. Sheety Configuration
- Create second sheet endpoint for users
- Copy both endpoints to `.env`:
  ```env
  SHEETY_PRICES_ENDPOINT=https://api.sheety.co/xxx/flightDeals/prices
  SHEETY_USERS_ENDPOINT=https://api.sheety.co/xxx/flightDeals/users
  ```

### 3. Email Setup (Gmail Example)

**Option A: Gmail App Password (Recommended)**
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in `.env`:
   ```env
   EMAIL_USER=your.email@gmail.com
   EMAIL_PASSWORD=your_16_char_app_password
   ```

**Option B: Other SMTP Providers**
```env
# Outlook
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# Yahoo
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Register New Users
```bash
python main.py
# Choose option 1
# Follow prompts to add users
```

**Example Session:**
```
First Name: Angela
Last Name: Yu
Email: angela@100daysofcode.com
Confirm Email: angela@100daysofcode.com
✅ Successfully added Angela Yu to Flight Club!

Register another user? (y/n): n
```

### Search & Notify
```bash
python main.py
# Choose option 2
```

**Output:**
```
--- Searching for Flight Deals ---
✓ Found deal: Paris for GBP42 (saves GBP8)
✓ Found deal: Berlin for GBP35 (saves GBP7)

✅ Found 2 deal(s)!
✓ Sent email to Angela (angela@100daysofcode.com)
✓ Sent email to John (john@example.com)
```

## Email Template Example

```
Subject: Flight Club Alert: 2 Cheap Flight(s) Found!

Hi Angela,

🎉 Flight Club - Today's Best Deals!

We found 2 amazing flight deal(s) for you:

1. Paris
   Price: GBP42 (save GBP8!)
   Route: London (LON) → Paris (CDG)
   Dates: 2024-12-15 to 2024-12-22
   Book: https://kiwi.com/deep?...

2. Berlin
   Price: GBP35 (save GBP7!)
   Route: London (STN) → Berlin (BER)
   Dates: 2024-12-20 to 2024-12-27
   Book: https://kiwi.com/deep?...

Happy travels! ✈️
- Flight Club Team
```

## Architecture

```
Day040/
├── main.py                    # CLI menu + orchestration
├── customer_acquisition.py    # User registration logic
├── data_manager.py           # Sheety API (prices + users)
├── flight_search.py          # Tequila API (unchanged)
├── notification_manager.py   # Email + SMS
├── .env                      # Secrets (gitignored)
└── README.md
```

## Validation Rules

**Email:**
- Must contain `@` and `.`
- Valid domain extension
- Regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

**Name:**
- Minimum 2 characters
- Letters, spaces, hyphens only
- Regex: `^[a-zA-Z\s\-]+$`

## Automation (Bonus)

**Run daily via cron:**
```cron
# Every day at 9 AM
0 9 * * * cd /path/to/project && python main.py <<< "2"
```

**Deploy on PythonAnywhere/Replit:**
- Set environment variables in platform settings
- Schedule task to run `main.py` with choice "2"

## Troubleshooting

**"SMTPAuthenticationError"**
- Gmail: Use App Password, not regular password
- Enable "Less secure app access" (not recommended)

**"Email not sent"**
- Check SMTP_SERVER and SMTP_PORT
- Verify EMAIL_USER and EMAIL_PASSWORD
- Test with: `telnet smtp.gmail.com 587`

**"No users registered"**
- Run option 1 first to add users
- Check SHEETY_USERS_ENDPOINT URL
- Verify sheet has "users" tab

## Comparison: Day 39 vs Day 40

| Feature | Day 39 | Day 40 |
|---------|--------|--------|
| Users | 1 (you) | Unlimited |
| Notification | SMS (Twilio) | Email (SMTP) |
| User Management | N/A | Google Sheets |
| Validation | N/A | Email + Name regex |
| Scalability | Personal | Product-ready |

## Business Model Ideas

**Free Tier:**
- Weekly deal emails
- Up to 5 destinations

**Premium ($5/month):**
- Daily emails
- Unlimited destinations
- Priority alerts (first to know)
- Custom price thresholds

## Next Steps

- **Day 41+**: Add web interface (Flask/Django)
- **Deployment**: Host on Heroku/Railway
- **Marketing**: Create landing page
- **Monetization**: Stripe integration for premium tier

## Inspiration

Based on real services like:
- Jack's Flight Club
- Scott's Cheap Flights
- Going (formerly Scott's Cheap Flights)

These companies charge $50-100/year for email alerts. You just built the core functionality in Python! 🚀