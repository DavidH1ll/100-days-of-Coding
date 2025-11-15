# Day 36 - Stock News Monitor

A Python-based stock monitoring system inspired by Bloomberg terminals. Tracks stock price changes and sends alerts with relevant news when significant fluctuations occur.

## Features

- **Stock Price Monitoring**: Fetches daily closing prices using Alpha Vantage API
- **Percentage Change Calculation**: Compares latest close to previous day
- **News Integration**: Retrieves relevant articles via NewsAPI when threshold exceeded
- **Dual Alert Methods**: Supports both SMS (Twilio) and Email notifications
- **Dry-Run Mode**: Preview alerts without sending
- **Configurable Thresholds**: Set custom percentage change triggers

## APIs Used

### 1. Alpha Vantage (Stock Prices)
- **Purpose**: Fetch daily stock time series data
- **Free Tier**: 25 requests/day
- **Get Key**: https://www.alphavantage.co/support/#api-key

### 2. NewsAPI (Company News)
- **Purpose**: Retrieve recent news articles
- **Free Tier**: 100 requests/day (developer plan)
- **Get Key**: https://newsapi.org/register

### 3. Twilio (SMS - Optional)
- **Purpose**: Send SMS alerts
- **Free Trial**: Test credits available
- **Get Credentials**: https://www.twilio.com/try-twilio

## Setup

### 1. Install Dependencies
```powershell
pip install requests python-dotenv twilio
```

### 2. Get API Keys
- Sign up for Alpha Vantage and get your API key
- Register for NewsAPI and get your API key
- (Optional) Sign up for Twilio for SMS alerts

### 3. Configure Environment
Copy `.env.example` to `.env` and fill in your values:

```env
# Stock to monitor
STOCK_SYMBOL=TSLA
COMPANY_NAME=Tesla Inc
PRICE_CHANGE_THRESHOLD=5.0

# API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
NEWS_API_KEY=your_news_api_key

# For SMS (optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_FROM=+1234567890
TWILIO_PHONE_TO=+1234567890

# For Email (alternative)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
TO_EMAIL=recipient@example.com

# Settings
DRY_RUN=true
USE_SMS=false
MAX_NEWS_ARTICLES=3
```

## Usage

### Dry-Run (Preview Alert)
```powershell
python main.py --dry-run
```

### Live Monitoring (Send Real Alerts)
Set `DRY_RUN=false` in `.env`, then:
```powershell
python main.py
```

### From Project Root
```powershell
python ".\100 days of Coding\Day036\main.py" --dry-run
```

## How It Works

1. **Fetch Stock Data**: Retrieves daily time series for configured symbol
2. **Calculate Change**: Compares latest close to previous close
3. **Check Threshold**: If absolute change ≥ threshold percentage:
   - Fetches recent news articles about the company
   - Formats alert with price data and news headlines
   - Sends notification via SMS or Email
4. **Alert Format**:
   ```
   TSLA Stock Alert
   🔺 6.32% change detected
   
   Previous close (2025-11-14): $245.50
   Latest close (2025-11-15): $261.02
   Change: +$15.52
   
   Recent News:
   1. Tesla announces new factory in Texas
      Source: Reuters
      https://...
   ```

## Project Structure

```
Day036/
├── main.py              # Orchestrator - checks stock, fetches news, sends alert
├── stock_api.py         # Alpha Vantage integration
├── news_api.py          # NewsAPI integration
├── notifications.py     # SMS (Twilio) and Email handlers
├── .env.example         # Template for environment variables
├── .env                 # Your actual credentials (gitignored)
└── README.md
```

## Testing Individual Modules

Each module has a `__main__` block for standalone testing:

```powershell
# Test stock fetching
python stock_api.py

# Test news fetching
python news_api.py

# Test notifications
python notifications.py
```

## Customization

### Monitor Different Stocks
Edit `.env`:
```env
STOCK_SYMBOL=AAPL
COMPANY_NAME=Apple Inc
```

### Adjust Sensitivity
Lower threshold = more alerts:
```env
PRICE_CHANGE_THRESHOLD=2.0
```

### Switch to SMS
```env
USE_SMS=true
DRY_RUN=false
```

## Rate Limits

- **Alpha Vantage**: 25 calls/day (free tier)
- **NewsAPI**: 100 calls/day (developer tier)
- **Twilio**: Trial credits or pay-as-you-go

⚠ **Tip**: Run once per day (e.g., after market close) to stay within limits.

## Automation (Optional)

### Windows Task Scheduler
1. Create a batch file `run_stock_monitor.bat`:
   ```batch
   cd "D:\Visual Studio Projects\100 days of Coding\Day036"
   .venv\Scripts\python.exe main.py
   ```
2. Schedule it to run daily at market close (4:00 PM EST)

### Linux/Mac Cron
```bash
0 16 * * 1-5 cd ~/projects/Day036 && python3 main.py
```

## Troubleshooting

**"ALPHA_VANTAGE_API_KEY not set"**
- Ensure `.env` file exists in Day036 folder
- Check API key is correctly copied (no extra spaces)

**"Note: Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute"**
- You hit the rate limit; wait 1 minute and try again

**401 Unauthorized (NewsAPI)**
- Verify your NewsAPI key is active
- Free tier may have restrictions on date range

**Twilio errors**
- Verify phone numbers are in E.164 format (+1234567890)
- Check account has credits

## Future Enhancements

- Support multiple stock symbols
- Historical trend analysis
- Telegram bot integration
- Web dashboard (Flask)
- Technical indicator alerts (RSI, MACD)
- Portfolio tracking

---

Built as part of 100 Days of Code - Day 36
