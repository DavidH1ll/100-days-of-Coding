"""
Day 47 - Amazon Price Tracker Bot

Build a bot that monitors Amazon product prices and sends email alerts
when prices drop below a target price.

Project Goals:
1. Scrape Amazon product pages to extract current price
2. Compare price against target price
3. Send email alerts when price drops below target
4. Support monitoring multiple products
5. Log price history and tracking activity
6. Handle errors gracefully (blocking, price parsing issues)

The bot can be scheduled to run daily (e.g., via cron job or task scheduler)
to continuously monitor prices and notify you when deals become available.

Note: Amazon actively blocks automated requests. Consider using:
- Proper User-Agent headers
- Delays between requests
- Product APIs instead of scraping (if available)
- Proxy services for large-scale monitoring
- Manual URL checks for critical products
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from datetime import datetime
import time

# ============================================================================
# Configuration
# ============================================================================

# Email Configuration
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'your_email@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'your_app_password')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'your_email@gmail.com')

# SMTP Configuration (Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRICE_HISTORY_FILE = os.path.join(SCRIPT_DIR, 'price_history.json')

# ============================================================================
# Product Price Scraper
# ============================================================================

def scrape_amazon_price(product_url, headers=None):
    """
    Scrape the current price from an Amazon product page.
    
    Args:
        product_url: Full Amazon product URL
        headers: Optional custom headers (to avoid blocking)
    
    Returns:
        Dictionary with price and other product info, or None if failed
    """
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    try:
        print(f"[DOWNLOAD] Fetching product page...")
        print(f"[URL] {product_url}\n")
        
        # Add delay to avoid aggressive blocking
        time.sleep(2)
        
        # Fetch the page
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("[OK] Page fetched successfully!\n")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple selectors for price (Amazon uses various class names)
        price = None
        price_selectors = [
            {'class_': 'a-price-whole'},
            {'class_': 'a-price-symbol'},
            {'id': 'priceblock_dealprice'},
            {'id': 'priceblock_ourprice'},
        ]
        
        print("[SEARCH] Searching for price on page...")
        
        # Method 1: Look for price in specific containers
        price_element = soup.find('span', class_='a-price-whole')
        if price_element:
            price_text = price_element.get_text(strip=True)
            print(f"[FOUND] Price element: {price_text}")
            try:
                # Remove currency symbols and convert to float
                price = float(price_text.replace('$', '').replace(',', ''))
                print(f"[OK] Parsed price: ${price:.2f}\n")
            except ValueError:
                print(f"[ERROR] Could not parse price: {price_text}\n")
                price = None
        
        # Method 2: Try alternative selectors if first method fails
        if not price:
            price_container = soup.find('div', {'data-a-color': 'price'})
            if price_container:
                price_text = price_container.get_text(strip=True)
                try:
                    price = float(price_text.replace('$', '').replace(',', ''))
                    print(f"[OK] Parsed price (alt method): ${price:.2f}\n")
                except ValueError:
                    pass
        
        # Get product title
        title = None
        title_element = soup.find('span', {'id': 'productTitle'})
        if title_element:
            title = title_element.get_text(strip=True)
        
        if price or title:
            return {
                'price': price,
                'title': title,
                'url': product_url,
                'timestamp': datetime.now().isoformat()
            }
        else:
            print("[WARNING] Could not extract price and title from page.")
            print("[INFO] Amazon may have updated their HTML structure.")
            print("[INFO] Current selectors may need updating.\n")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        print("[INFO] Amazon may be blocking automated requests.\n")
        return None
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}\n")
        return None


# ============================================================================
# Email Alert System
# ============================================================================

def send_price_alert_email(product_info, target_price, current_price):
    """
    Send an email alert when price drops below target.
    
    Args:
        product_info: Dictionary with product details
        target_price: Target price threshold
        current_price: Current product price
    
    Returns:
        True if email sent successfully, False otherwise
    """
    print("[EMAIL] Preparing email alert...\n")
    
    try:
        # Check if credentials are configured
        if SENDER_EMAIL == 'your_email@gmail.com' or SENDER_PASSWORD == 'your_app_password':
            print("[WARNING] Email credentials not configured!")
            print("[INFO] To send emails, set environment variables:")
            print("   - SENDER_EMAIL: Your Gmail address")
            print("   - SENDER_PASSWORD: Gmail app-specific password")
            print("   - RECIPIENT_EMAIL: Target email address")
            print("[INFO] To get app password:")
            print("   1. Enable 2-Factor Authentication on Gmail")
            print("   2. Go to myaccount.google.com/apppasswords")
            print("   3. Generate a password for 'Mail' and 'Windows Computer'")
            print("   4. Use this password as SENDER_PASSWORD\n")
            return False
        
        # Create email message
        subject = f"[PRICE ALERT] {product_info['title']}: NOW ${current_price:.2f}!"
        
        body = f"""
Dear Shopper,

Great news! The product you're tracking has dropped to your target price!

PRODUCT: {product_info['title']}
CURRENT PRICE: ${current_price:.2f}
YOUR TARGET PRICE: ${target_price:.2f}
SAVINGS: ${target_price - current_price:.2f}

Now is the time to buy!

PRODUCT LINK:
{product_info['url']}

[ACTION REQUIRED]
Click the link above to view the product and complete your purchase.
Note: Prices can change rapidly, so act quickly!

---
Amazon Price Tracker Bot
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Create MIME message
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECIPIENT_EMAIL
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        
        # Send email
        print(f"[EMAIL] Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print("[OK] Secure connection established.\n")
            
            print(f"[EMAIL] Authenticating with {SENDER_EMAIL}...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("[OK] Authentication successful.\n")
            
            print(f"[EMAIL] Sending alert to {RECIPIENT_EMAIL}...")
            server.send_message(message)
            print("[OK] Email sent successfully!\n")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Email authentication failed!")
        print("[INFO] Check your email credentials.\n")
        return False
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP error: {e}\n")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}\n")
        return False


# ============================================================================
# Price History Tracking
# ============================================================================

def load_price_history():
    """
    Load price history from JSON file.
    
    Returns:
        Dictionary with product tracking data
    """
    if os.path.exists(PRICE_HISTORY_FILE):
        try:
            with open(PRICE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARNING] Could not load price history: {e}")
            return {}
    return {}


def save_price_history(history):
    """
    Save price history to JSON file.
    
    Args:
        history: Dictionary with price tracking data
    """
    try:
        with open(PRICE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"[WARNING] Could not save price history: {e}")


def update_price_record(product_url, price, title):
    """
    Update price record for a product.
    
    Args:
        product_url: Product URL (used as key)
        price: Current price
        title: Product title
    
    Returns:
        Updated history dictionary
    """
    history = load_price_history()
    
    # Create or update product entry
    if product_url not in history:
        history[product_url] = {
            'title': title,
            'prices': [],
            'alert_sent': False
        }
    
    # Add price record
    history[product_url]['prices'].append({
        'price': price,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last 30 records to avoid file bloat
    if len(history[product_url]['prices']) > 30:
        history[product_url]['prices'] = history[product_url]['prices'][-30:]
    
    save_price_history(history)
    return history


# ============================================================================
# Price Comparison and Tracking
# ============================================================================

def track_product_price(product_url, target_price, product_name=None):
    """
    Main function to track a product and send alerts.
    
    Args:
        product_url: Full Amazon product URL
        target_price: Target price for alert
        product_name: Optional product name for display
    
    Returns:
        Dictionary with tracking results
    """
    print("=" * 70)
    print("Amazon Price Tracker Bot".center(70))
    print("=" * 70)
    print()
    
    print(f"[TRACK] Monitoring: {product_name or 'Product'}")
    print(f"[TARGET] Target Price: ${target_price:.2f}\n")
    
    # Scrape current price
    product_info = scrape_amazon_price(product_url)
    
    if not product_info or product_info['price'] is None:
        print("[ERROR] Could not retrieve price. Tracking failed.\n")
        return {
            'success': False,
            'message': 'Failed to retrieve price',
            'url': product_url
        }
    
    current_price = product_info['price']
    title = product_info['title'] or product_name or 'Product'
    
    print("=" * 70)
    print("Price Analysis".center(70))
    print("=" * 70)
    print()
    print(f"Current Price: ${current_price:.2f}")
    print(f"Target Price: ${target_price:.2f}")
    
    # Calculate savings
    if current_price <= target_price:
        savings = target_price - current_price
        percentage = (savings / target_price) * 100
        print(f"Status: [BELOW TARGET] Savings: ${savings:.2f} ({percentage:.1f}%)\n")
        
        # Update price record
        history = update_price_record(product_url, current_price, title)
        
        # Send alert if not already sent
        if not history[product_url]['alert_sent']:
            print("[ALERT] Price is below target! Sending email alert...\n")
            email_sent = send_price_alert_email(product_info, target_price, current_price)
            
            # Mark alert as sent
            if email_sent:
                history[product_url]['alert_sent'] = True
                save_price_history(history)
                
                return {
                    'success': True,
                    'message': 'Price alert sent',
                    'current_price': current_price,
                    'target_price': target_price,
                    'savings': savings,
                    'url': product_url
                }
        else:
            print("[INFO] Alert already sent for this price point.\n")
    else:
        difference = current_price - target_price
        print(f"Status: [ABOVE TARGET] Need: ${difference:.2f} more drop\n")
        
        # Update price record
        update_price_record(product_url, current_price, title)
    
    print("=" * 70)
    print()
    
    return {
        'success': True,
        'message': 'Price tracked successfully',
        'current_price': current_price,
        'target_price': target_price,
        'alert_needed': current_price <= target_price,
        'url': product_url
    }


def display_price_history(product_url):
    """
    Display price history for a product.
    
    Args:
        product_url: Product URL
    """
    history = load_price_history()
    
    if product_url not in history:
        print("[INFO] No price history available for this product.\n")
        return
    
    product = history[product_url]
    
    print("=" * 70)
    print("Price History".center(70))
    print("=" * 70)
    print()
    print(f"Product: {product['title']}")
    print(f"Total Records: {len(product['prices'])}\n")
    
    if product['prices']:
        print("Recent Prices (newest first):")
        print("-" * 70)
        
        for record in reversed(product['prices'][-10:]):
            timestamp = datetime.fromisoformat(record['timestamp'])
            print(f"${record['price']:8.2f} | {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("-" * 70)
        
        # Show statistics
        prices = [r['price'] for r in product['prices']]
        print(f"\nPrice Statistics:")
        print(f"  Highest: ${max(prices):.2f}")
        print(f"  Lowest:  ${min(prices):.2f}")
        print(f"  Current: ${prices[-1]:.2f}")
        print(f"  Average: ${sum(prices)/len(prices):.2f}\n")


# ============================================================================
# Interactive Menu
# ============================================================================

def display_example_products():
    """
    Display example Amazon products for testing.
    These are generic examples - replace with actual Amazon URLs.
    """
    print("\n" + "=" * 70)
    print("Example Amazon Products".center(70))
    print("=" * 70)
    print()
    print("To test this tracker, use actual Amazon product URLs.")
    print("Example format:")
    print("  https://www.amazon.com/dp/B00000JHDX/")
    print("  https://www.amazon.com/Instant-Pot-Multi-Use-Pressure-Cooker/dp/B00FLYWNYQ/")
    print()
    print("Note: Amazon actively blocks automated requests.")
    print("If you encounter blocking issues:")
    print("  1. Add longer delays between requests")
    print("  2. Use different User-Agent headers")
    print("  3. Consider using browser automation (Selenium)")
    print("  4. Use official APIs if available")
    print("  5. Check if the product has an API endpoint\n")


def main():
    """
    Main program demonstrating the price tracker.
    """
    print()
    print("=" * 70)
    print("Amazon Price Tracker Bot - Demo".center(70))
    print("=" * 70)
    print()
    
    print("This bot monitors Amazon product prices and sends email alerts")
    print("when prices drop below your target price.\n")
    
    print("Features:")
    print("  - Scrape current Amazon product prices")
    print("  - Track price history")
    print("  - Compare against target price")
    print("  - Send email alerts when deal found")
    print("  - View price statistics and trends\n")
    
    display_example_products()
    
    print("=" * 70)
    print("Key Concepts Demonstrated:".center(70))
    print("=" * 70)
    print("""
1. Advanced Web Scraping
   - Handling website blocking and anti-scraping measures
   - Multiple selector strategies for robustness
   - User-Agent spoofing and header management
   - Error recovery and graceful degradation

2. Email Automation
   - SMTP protocol and secure connections
   - Gmail app-specific passwords
   - MIME multipart messages
   - Error handling for email delivery

3. Data Processing
   - Price parsing and validation
   - JSON file storage and retrieval
   - Data transformation and formatting
   - Statistical calculations

4. Scheduling Concepts
   - How to run bots at specific times
   - Task scheduler integration
   - Cron job setup for Linux/Mac
   - Persistent logging and history

5. Real-World Challenges
   - Website structure changes
   - Rate limiting and blocking
   - Session management
   - API alternatives to scraping

""")
    
    print("=" * 70)
    print("How to Use:".center(70))
    print("=" * 70)
    print("""
1. Find an Amazon product URL
2. Set your target price
3. Configure email credentials (environment variables):
   - SENDER_EMAIL: Your Gmail address
   - SENDER_PASSWORD: Gmail app password
   - RECIPIENT_EMAIL: Alert recipient

4. Run the tracker:
   result = track_product_price(url, target_price)

5. For automation, schedule this script to run daily using:
   - Windows Task Scheduler
   - Linux cron jobs
   - Cloud services (AWS Lambda, Google Cloud Functions)

""")
    
    print("=" * 70)
    print("Important Notes:".center(70))
    print("=" * 70)
    print("""
LEGAL & ETHICAL CONSIDERATIONS:
- Check Amazon's Terms of Service before scraping
- Respect robots.txt and rate limits
- Use appropriate delays between requests
- Consider using official APIs instead
- Do not overload Amazon's servers

TECHNICAL CHALLENGES:
- Amazon actively blocks automated requests
- HTML structure changes frequently
- JavaScript-rendered content requires special handling
- IP blocking may occur with aggressive scraping

SOLUTIONS:
- Use selenium/playwright for JavaScript rendering
- Rotate User-Agent strings
- Use proxy services for scale
- Implement exponential backoff retry logic
- Monitor for HTML changes and update selectors

ALTERNATIVES:
- Use Amazon Product Advertising API
- Use third-party price tracking APIs
- Try camelcamelcamel.com for price history
- Use browser extensions for real-time tracking

""")
    
    print("=" * 70)
    print()
    print("[INFO] Tracker demonstration complete!")
    print("[INFO] Ready to monitor products with actual URLs and credentials.\n")


if __name__ == "__main__":
    main()
