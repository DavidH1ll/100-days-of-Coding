# Day 047 - Amazon Price Tracker Bot

## Project Overview
Build a Python bot that monitors Amazon product prices and automatically sends email alerts when prices drop below your target price. This project combines web scraping, email automation, data persistence, and real-world problem-solving.

## Learning Objectives
- Advanced web scraping with error handling
- Email automation using SMTP
- JSON data persistence
- Price comparison logic
- Handling website blocking and anti-scraping measures
- Scheduling considerations for automated tasks
- Real-world application development

## Project Features

### 1. Price Scraper
- Extract current prices from Amazon product pages
- Parse HTML with multiple fallback selectors
- Extract product titles and details
- Handle Amazon's anti-scraping measures
- Graceful degradation on failures

### 2. Price Comparison Engine
- Compare current price against target price
- Calculate savings and percentages
- Track price history
- Display statistics

### 3. Email Alert System
- Send formatted email alerts
- Include product details and links
- Use Gmail SMTP with app-specific passwords
- Handle email authentication errors

### 4. Data Persistence
- Store price history in JSON
- Track alert status
- Keep last 30 price records per product
- Generate statistics from historical data

## Technical Architecture

### Dependencies
```
requests - HTTP library for web scraping
beautifulsoup4 - HTML parsing
smtplib - Built-in email library
json - Built-in data format
```

### Installation
```bash
pip install requests beautifulsoup4
```

Note: `smtplib` and `json` are part of Python's standard library.

## Key Concepts

### 1. Web Scraping Challenges

**Amazon's Anti-Scraping Measures:**
```python
# Problem: Amazon actively blocks bots
# Solution: Use realistic headers and delays

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive'
}

time.sleep(2)  # Delay between requests
response = requests.get(url, headers=headers, timeout=10)
```

**Why It Matters**: 
- Amazon detects bots by looking for suspicious request patterns
- Realistic User-Agent strings make requests appear human
- Delays reduce server load and avoid rate limiting
- Different headers simulate real browser requests

**Multiple Selector Strategy:**
```python
# Method 1: Try primary selector
price_element = soup.find('span', class_='a-price-whole')

# Method 2: Try alternative selector if primary fails
if not price_element:
    price_container = soup.find('div', {'data-a-color': 'price'})

# Method 3: Have multiple fallbacks ready
# This ensures robustness when Amazon updates HTML
```

### 2. Email Automation with SMTP

**Understanding SMTP (Simple Mail Transfer Protocol):**
```python
# Establish secure connection
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()              # Upgrade to TLS encryption
    server.login(email, password)  # Authenticate
    server.send_message(message)   # Send email
```

**Why It Matters**:
- SMTP is the standard protocol for sending emails
- `starttls()` encrypts the connection for security
- Gmail app-specific passwords are safer than account passwords
- MIME multipart allows rich formatted emails

**Gmail App Passwords:**
```
Why use app passwords?
- Regular password gives full account access
- App passwords are limited to specific applications
- Can be revoked without changing main password
- Enables 2FA while allowing app access

Setup:
1. Enable 2-Factor Authentication on Gmail
2. Go to myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Google generates a 16-character password
5. Use this password in SENDER_PASSWORD
```

**MIME Message Structure:**
```python
message = MIMEMultipart()
message['From'] = SENDER_EMAIL
message['To'] = RECIPIENT_EMAIL
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Result: A proper email with headers and body
```

### 3. Data Persistence with JSON

**Why JSON for Price History?**
```python
# Human-readable structure
{
    "https://amazon.com/product": {
        "title": "Product Name",
        "prices": [
            {
                "price": 99.99,
                "timestamp": "2024-11-23T15:30:00"
            },
            ...
        ],
        "alert_sent": false
    }
}
```

**Benefits**:
- Human-readable format
- Easy to parse with Python
- Lightweight and portable
- Can be easily shared or migrated
- No database setup required

**Price History Management:**
```python
# Keep only last 30 records to prevent bloat
if len(history[product_url]['prices']) > 30:
    history[product_url]['prices'] = \
        history[product_url]['prices'][-30:]
```

### 4. Price Comparison Logic

**Tracking State:**
```python
if current_price <= target_price:
    savings = target_price - current_price
    percentage = (savings / target_price) * 100
    
    if not history[product_url]['alert_sent']:
        # Send email only once per price point
        send_email()
        history[product_url]['alert_sent'] = True
```

**Why Alert Only Once?**
- Avoid email spam if price stays low
- Reset when price goes back up
- Prevents notification fatigue
- Improves user experience

### 5. Scheduling for Automation

**How to Run Daily (Different Approaches):**

**Windows Task Scheduler:**
```
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily at 9:00 AM)
4. Action: Start Program
   - Program: python.exe path
   - Arguments: C:\path\to\main.py
```

**Linux/Mac Cron Job:**
```bash
# Edit crontab
crontab -e

# Run daily at 9:00 AM
0 9 * * * /usr/bin/python3 /path/to/main.py

# Run every hour
0 * * * * /usr/bin/python3 /path/to/main.py
```

**Cloud Solutions:**
```
AWS Lambda: Trigger with CloudWatch Events
Google Cloud Functions: Scheduled triggers
Azure Functions: Timer triggers
```

### 6. Error Handling Strategy

**Network Errors:**
```python
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
    # Could retry with exponential backoff
    # Could use proxy service
    # Could log for manual review
```

**Email Errors:**
```python
except smtplib.SMTPAuthenticationError:
    print("Authentication failed")
    # Check credentials
    # Verify app password is correct
    
except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")
    # May be rate limited
    # May have temporary service issues
```

**Parsing Errors:**
```python
try:
    price = float(price_text.replace('$', '').replace(',', ''))
except ValueError:
    print(f"Could not parse price: {price_text}")
    # HTML structure may have changed
    # May need selector updates
```

## Setup Instructions

### 1. Get Gmail App Password

1. Enable 2-Factor Authentication on your Google Account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Google generates a 16-character password
5. Copy this password (spaces will be removed automatically)

### 2. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:SENDER_EMAIL = "your_email@gmail.com"
$env:SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"
$env:RECIPIENT_EMAIL = "recipient@gmail.com"
```

**Windows (Permanent - Command Prompt):**
```cmd
setx SENDER_EMAIL "your_email@gmail.com"
setx SENDER_PASSWORD "xxxx xxxx xxxx xxxx"
setx RECIPIENT_EMAIL "recipient@gmail.com"
```

**Linux/Mac (Bash):**
```bash
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="xxxx xxxx xxxx xxxx"
export RECIPIENT_EMAIL="recipient@gmail.com"
```

### 3. Run the Tracker

```python
from main import track_product_price

# Example usage
product_url = "https://www.amazon.com/dp/B00000JHDX/"
target_price = 99.99

result = track_product_price(product_url, target_price, "Instant Pot")
```

## Usage Examples

### Basic Price Check
```python
result = track_product_price(
    product_url="https://amazon.com/dp/B00000JHDX/",
    target_price=99.99,
    product_name="Instant Pot"
)

print(result)
# {
#     'success': True,
#     'message': 'Price tracked successfully',
#     'current_price': 105.50,
#     'target_price': 99.99,
#     'alert_needed': False,
#     'url': '...'
# }
```

### View Price History
```python
display_price_history("https://amazon.com/dp/B00000JHDX/")

# Output:
# Price Statistics:
#   Highest: $125.99
#   Lowest:  $95.50
#   Current: $105.50
#   Average: $110.23
```

### Automated Daily Check
```python
# Save as scheduled_tracker.py
import schedule
import time
from main import track_product_price

def job():
    track_product_price(
        "https://amazon.com/dp/B00000JHDX/",
        99.99,
        "Instant Pot"
    )

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Real-World Challenges & Solutions

### Challenge 1: Amazon Blocks Requests

**Symptoms**: 
- 403 Forbidden errors
- Empty price results
- HTML structure completely different

**Solutions**:
```python
# Add delays
time.sleep(random.randint(2, 5))

# Rotate user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    # More agents...
]
headers['User-Agent'] = random.choice(user_agents)

# Use proxies (requires paid service)
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}
response = requests.get(url, proxies=proxies)

# Use browser automation
# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get(url)
```

### Challenge 2: HTML Structure Changes

**Symptoms**:
- Price not found
- Wrong price extracted
- Script suddenly fails

**Solution**:
```python
# Implement selector versioning
SELECTORS = {
    'v1': {'class_': 'a-price-whole'},
    'v2': {'class_': 'a-price-symbol'},
    'v3': {'id': 'priceblock_dealprice'},
}

for version, selector in SELECTORS.items():
    element = soup.find('span', selector)
    if element:
        price = parse_price(element.get_text())
        break
```

### Challenge 3: Email Not Sending

**Symptoms**:
- SMTPAuthenticationError
- Connection timeouts
- Rate limiting (429 error)

**Solutions**:
```python
# Verify credentials
print(f"Using: {SENDER_EMAIL}")
print("Check that app password is correct")

# Gmail specific limits
# - 500 emails per day
# - Rate limit: ~1 email per second

# Add retry logic
max_retries = 3
for attempt in range(max_retries):
    try:
        # Send email
        break
    except smtplib.SMTPException:
        if attempt < max_retries - 1:
            time.sleep(5)  # Wait before retry
        else:
            raise
```

## Extensions & Enhancements

### 1. Multi-Product Tracking
```python
products = [
    {"url": "...", "target": 99.99},
    {"url": "...", "target": 199.99},
]

for product in products:
    track_product_price(product['url'], product['target'])
```

### 2. Price Drop Notifications
```python
# Alert if price drops by percentage
if (previous_price - current_price) / previous_price > 0.10:  # 10% drop
    send_price_alert_email(...)
```

### 3. Web Dashboard
```python
# Flask app to view price history
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/prices')
def show_prices():
    history = load_price_history()
    return render_template('prices.html', history=history)
```

### 4. Browser Automation
```python
# Handle JavaScript-rendered prices
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(product_url)
price_element = driver.find_element("class name", "a-price-whole")
price = parse_price(price_element.text)
driver.quit()
```

### 5. Advanced Scheduling
```python
import schedule

schedule.every().day.at("09:00").do(check_prices)
schedule.every(2).hours.do(check_urgent_products)
schedule.every().monday.at("10:00").do(weekly_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Files Created

```
Day047/
├── main.py                      # Main application
├── price_history.json          # Generated price data
└── README.md                    # This file
```

## Important Notes

### Legal & Ethical Considerations
- Check Amazon's Terms of Service
- Respect robots.txt
- Don't overload servers
- Consider using official APIs
- Be respectful of bandwidth

### Technical Limitations
- Amazon actively blocks bots
- HTML changes frequently
- IP addresses may be blocked
- Complex JavaScript may need Selenium
- Rate limiting may apply

### Alternatives
- Use Amazon Product Advertising API
- Try camelcamelcamel.com (price history)
- Use browser extensions
- Third-party price tracking services
- Official merchant APIs

## Best Practices Applied

✅ Multiple selector strategies for robustness
✅ Proper error handling and recovery
✅ Security: App passwords instead of account passwords
✅ Data persistence with JSON
✅ Email formatting and structure
✅ User-Agent spoofing for realistic requests
✅ Delays to avoid aggressive blocking
✅ Graceful degradation on failures
✅ Price tracking state management
✅ Comprehensive logging and feedback

## Skills Demonstrated

✅ Advanced web scraping techniques
✅ Anti-scraping countermeasure handling
✅ Email automation and SMTP
✅ JSON data serialization
✅ Price parsing and validation
✅ Multi-level error handling
✅ Schedule automation concepts
✅ Email security and credentials
✅ State management
✅ Real-world application development

## Summary

Day 047 teaches how to build practical, real-world applications that solve actual problems. The Amazon Price Tracker demonstrates web scraping challenges, email automation, data persistence, and the importance of handling edge cases and errors. These concepts apply to many other projects: stock price tracking, hotel rate monitoring, flight price alerts, and more.

The project emphasizes that while web scraping is a powerful tool, it must be used responsibly and ethically. Understanding the challenges and alternatives ensures you can make the right choice for each situation.

