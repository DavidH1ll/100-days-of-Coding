"""
Example: How to Use the Amazon Price Tracker

This script demonstrates how to use the price tracker bot
to monitor Amazon products.
"""

from main import track_product_price, display_price_history

# ============================================================================
# Example 1: Basic Price Tracking
# ============================================================================

def example_basic_tracking():
    """
    Example: Track a single product
    """
    print("\n" + "=" * 70)
    print("Example 1: Basic Price Tracking".center(70))
    print("=" * 70 + "\n")
    
    # Replace these with actual Amazon product URLs
    product_url = "https://www.amazon.com/dp/B00000JHDX/"
    target_price = 99.99
    product_name = "Instant Pot"
    
    # Track the product
    result = track_product_price(product_url, target_price, product_name)
    
    print(f"Result: {result}\n")


# ============================================================================
# Example 2: View Price History
# ============================================================================

def example_price_history():
    """
    Example: View price history for a product
    """
    print("\n" + "=" * 70)
    print("Example 2: View Price History".center(70))
    print("=" * 70 + "\n")
    
    product_url = "https://www.amazon.com/dp/B00000JHDX/"
    
    # Display price history
    display_price_history(product_url)


# ============================================================================
# Example 3: Multiple Products
# ============================================================================

def example_multiple_products():
    """
    Example: Track multiple products at once
    """
    print("\n" + "=" * 70)
    print("Example 3: Track Multiple Products".center(70))
    print("=" * 70 + "\n")
    
    products = [
        {
            "url": "https://www.amazon.com/dp/B00000JHDX/",
            "target": 99.99,
            "name": "Instant Pot"
        },
        {
            "url": "https://www.amazon.com/dp/ANOTHERPRODUCT/",
            "target": 199.99,
            "name": "Another Product"
        },
    ]
    
    print(f"Tracking {len(products)} products...\n")
    
    for product in products:
        print(f"Checking: {product['name']}")
        result = track_product_price(
            product['url'],
            product['target'],
            product['name']
        )
        
        if result['success']:
            print(f"  Current: ${result['current_price']:.2f}")
            print(f"  Target:  ${result['target_price']:.2f}\n")
        else:
            print(f"  Error: {result['message']}\n")


# ============================================================================
# How to Schedule Daily Checks
# ============================================================================

def example_scheduled_tracking():
    """
    Example: How to schedule daily price checks
    
    Note: Requires 'schedule' library
    pip install schedule
    """
    print("\n" + "=" * 70)
    print("Example 4: Scheduled Daily Tracking".center(70))
    print("=" * 70 + "\n")
    
    print("To run price checks automatically, use one of these methods:\n")
    
    print("METHOD 1: Using APScheduler library")
    print("-" * 70)
    print("""
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def check_prices():
    track_product_price(url, target_price)

scheduler.add_job(check_prices, 'cron', hour=9, minute=0)
scheduler.start()
    """)
    
    print("\nMETHOD 2: Windows Task Scheduler")
    print("-" * 70)
    print("""
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start Program
   Program: C:\\Python311\\python.exe
   Arguments: C:\\path\\to\\tracker.py
    """)
    
    print("\nMETHOD 3: Linux Cron Job")
    print("-" * 70)
    print("""
crontab -e

# Add this line to run daily at 9 AM:
0 9 * * * /usr/bin/python3 /home/user/price_tracker.py
    """)
    
    print("\nMETHOD 4: Cloud Services")
    print("-" * 70)
    print("""
AWS Lambda + CloudWatch Events
Google Cloud Functions + Cloud Scheduler
Azure Functions + Timer Triggers
    """)


# ============================================================================
# Email Configuration Guide
# ============================================================================

def example_email_setup():
    """
    Example: How to set up Gmail for email alerts
    """
    print("\n" + "=" * 70)
    print("Example 5: Email Configuration".center(70))
    print("=" * 70 + "\n")
    
    print("STEP 1: Enable 2-Factor Authentication")
    print("-" * 70)
    print("""
1. Go to myaccount.google.com
2. Click 'Security' in left menu
3. Scroll to '2-Step Verification'
4. Click 'Get Started' and follow prompts
    """)
    
    print("\nSTEP 2: Create App Password")
    print("-" * 70)
    print("""
1. Go to myaccount.google.com/apppasswords
2. Select 'Mail' for app
3. Select 'Windows Computer' for device
4. Click 'Generate'
5. Copy the 16-character password
    """)
    
    print("\nSTEP 3: Set Environment Variables")
    print("-" * 70)
    print("""
Windows (PowerShell):
$env:SENDER_EMAIL = "your_email@gmail.com"
$env:SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"
$env:RECIPIENT_EMAIL = "recipient@gmail.com"

Windows (Permanent - Command Prompt):
setx SENDER_EMAIL "your_email@gmail.com"
setx SENDER_PASSWORD "xxxx xxxx xxxx xxxx"
setx RECIPIENT_EMAIL "recipient@gmail.com"

Linux/Mac:
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="xxxx xxxx xxxx xxxx"
export RECIPIENT_EMAIL="recipient@gmail.com"
    """)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("Amazon Price Tracker - Usage Examples".center(70))
    print("=" * 70)
    print()
    
    print("This script demonstrates how to use the price tracker.\n")
    
    print("Available examples:")
    print("  1. Basic price tracking for one product")
    print("  2. View price history and statistics")
    print("  3. Track multiple products")
    print("  4. Schedule daily automated checks")
    print("  5. Email configuration guide\n")
    
    print("=" * 70)
    print()
    
    # Show all examples
    print("NOTE: These are examples of how to use the tracker.")
    print("Modify with your actual Amazon product URLs and target prices.\n")
    
    print("IMPORTANT: Email alerts require:")
    print("  1. Gmail account with 2-Factor Authentication enabled")
    print("  2. App-specific password generated")
    print("  3. Environment variables configured\n")
    
    print("For production use:")
    print("  1. Replace example URLs with real Amazon product URLs")
    print("  2. Configure email credentials (see example_email_setup)")
    print("  3. Set up scheduling (see example_scheduled_tracking)")
    print("  4. Test with one product before scaling to multiple\n")
    
    print("=" * 70)
    print()

    # Show example guides (these don't require actual URLs)
    example_scheduled_tracking()
    example_email_setup()
    
    print("\n" + "=" * 70)
    print("Ready to start tracking prices!".center(70))
    print("=" * 70 + "\n")
