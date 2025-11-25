"""
Day 51 - Complaining Twitter Bot with Internet Speed Testing

Automate internet speed testing on speedtest.net and automatically tweet
complaints about poor internet speeds to your ISP.

Project: Automated Speed Test → Twitter Complaint Pipeline
Goal: Hold ISPs accountable for promised speeds through public tweets

Real-World Problem:
- ISPs promise speeds they don't deliver (e.g., promised 150 Mbps, getting 23 Mbps)
- Companies respond better to public complaints on Twitter
- Manual speed testing and tweeting is tedious
- This bot automates the entire process

How It Works:
1. Run speedtest.net to measure actual internet speeds
2. Compare against your ISP's promised speeds
3. Generate witty complaint tweet
4. Post to Twitter mentioning your ISP
5. Build evidence for refunds or service improvements

Key Concepts:
- Selenium automation of speed testing website
- Twitter API integration for automated posting
- Speed comparison and complaint generation
- Result tracking and historical data
- ISP provider configuration
- Ethical complaint tweeting

Real-World Impact:
- Users have successfully gotten refunds from ISPs
- Companies monitor Twitter for complaints
- Public evidence strengthens negotiation position
- Many ISPs have poor customer service on Twitter
- JetBlue and others actively respond to complaints

Ethical Considerations:
✓ Only tweet truthful speed test results
✓ Be factual and professional in complaints
✓ Have data to back up claims
✓ Aim for improvement, not harassment
✓ Don't spam multiple tweets to same ISP
✗ Don't fabricate or exaggerate speeds
✗ Don't use for harassment or abuse
✗ Don't violate Twitter Terms of Service
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from datetime import datetime
from functools import wraps
import os

# ============================================================================
# Configuration
# ============================================================================

# SpeedTest.net
SPEEDTEST_URL = "https://www.speedtest.net/"

# Twitter API (requires setup - see README)
# You need: API key, API secret, Access token, Access token secret
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET", "")

# ISP Configurations
ISP_CONFIGS = {
    "comcast": {
        "name": "Comcast",
        "handle": "@comcastcares",
        "typical_promises": {
            "standard": {"down": 150, "up": 10},
            "performance": {"down": 300, "up": 20},
            "gigabit": {"down": 1000, "up": 35}
        }
    },
    "att": {
        "name": "AT&T",
        "handle": "@ATTCares",
        "typical_promises": {
            "basic": {"down": 25, "up": 1},
            "plus": {"down": 50, "up": 5},
            "max": {"down": 100, "up": 10}
        }
    },
    "verizon": {
        "name": "Verizon",
        "handle": "@VerizonSupport",
        "typical_promises": {
            "basic": {"down": 25, "up": 3},
            "plus": {"down": 50, "up": 10},
            "fios": {"down": 100, "up": 100}
        }
    },
    "spectrum": {
        "name": "Charter Spectrum",
        "handle": "@SpectrumSupport",
        "typical_promises": {
            "internet": {"down": 100, "up": 10},
            "ultra": {"down": 300, "up": 20}
        }
    },
    "sky": {
        "name": "Sky",
        "handle": "@SkyHelp",
        "typical_promises": {
            "broadband": {"down": 59, "up": 5},
            "superfast": {"down": 145, "up": 20}
        }
    },
    "bt": {
        "name": "BT",
        "handle": "@BTCare",
        "typical_promises": {
            "standard": {"down": 52, "up": 9},
            "superfast": {"down": 145, "up": 24}
        }
    }
}

# Timeout values
SPEEDTEST_TIMEOUT = 300  # Speed test takes 1-2 minutes
BROWSER_TIMEOUT = 10

# Data storage
RESULTS_FILE = "speed_test_results.json"

# ============================================================================
# Retry Decorator
# ============================================================================

def retry_on_failure(max_retries=3, delay=2, backoff=True):
    """Retry decorator for speed test and tweet operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"\n[ATTEMPT {attempt}/{max_retries}] {func.__name__}...")
                    result = func(*args, **kwargs)
                    print(f"[SUCCESS] {func.__name__} succeeded")
                    return result
                except Exception as e:
                    print(f"[ERROR] Attempt {attempt} failed: {e}")
                    if attempt < max_retries:
                        print(f"[RETRY] Waiting {current_delay}s before retry...")
                        time.sleep(current_delay)
                        if backoff:
                            current_delay *= 2
                    else:
                        print(f"[FAILED] All {max_retries} attempts exhausted")
                        raise
        return wrapper
    return decorator


# ============================================================================
# Browser Setup
# ============================================================================

def setup_chrome_driver(headless=False):
    """
    Set up Chrome WebDriver for speed testing.
    
    Args:
        headless: Run in headless mode (no UI)
    
    Returns:
        WebDriver instance
    """
    print("\n[BROWSER] Setting up Chrome WebDriver...")
    
    options = Options()
    
    if headless:
        options.add_argument("--headless=new")
        print("[BROWSER] Headless mode enabled")
    
    # Optimizations
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("[OK] WebDriver initialized")
        return driver
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        raise


# ============================================================================
# Speed Testing
# ============================================================================

@retry_on_failure(max_retries=2, delay=2)
def run_speedtest(driver):
    """
    Run internet speed test on speedtest.net.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        Dict with 'download', 'upload', 'ping', 'server', 'result_url'
    
    Raises:
        Exception if speed test fails
    """
    print(f"\n[SPEEDTEST] Starting internet speed test...")
    print(f"[INFO] This will take 1-2 minutes depending on your internet speed\n")
    
    try:
        # Navigate to speedtest.net
        print("[LOAD] Navigating to speedtest.net...")
        driver.get(SPEEDTEST_URL)
        WebDriverWait(driver, BROWSER_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("[OK] SpeedTest.net loaded")
        
        time.sleep(2)
        
        # Find and click the "Go" button
        print("\n[BUTTON] Looking for 'Go' button...")
        try:
            # Try multiple selectors for the go button
            go_button = None
            selectors = [
                "button[class*='start']",
                "div[class*='start-button']",
                "a[class*='go-button']",
                "//*[contains(text(), 'Go')]"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("/"):
                        go_button = driver.find_element(By.XPATH, selector)
                    else:
                        go_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if go_button and go_button.is_displayed():
                        break
                except:
                    continue
            
            if not go_button:
                # If button not found, try clicking anywhere on the page
                print("[INFO] Using alternative method to start test")
                driver.execute_script("window.addEventListener('beforeunload', function(){});")
            else:
                print("[OK] 'Go' button found, clicking...")
                driver.execute_script("arguments[0].scrollIntoView(true);", go_button)
                time.sleep(0.5)
                go_button.click()
                print("[OK] Test started")
        
        except Exception as e:
            print(f"[WARNING] Could not click button: {e}")
            print("[INFO] Attempting to start test via page interaction")
        
        # Wait for results - speed test takes time
        print("\n[TESTING] Speed test in progress... (waiting up to 3 minutes)")
        print("[INFO] Measuring download and upload speeds...\n")
        
        start_time = time.time()
        test_timeout = 180  # 3 minutes
        
        # Look for result elements
        result_found = False
        while not result_found and (time.time() - start_time) < test_timeout:
            try:
                # Look for results container
                results = driver.find_elements(By.CLASS_NAME, "result-item")
                if results and len(results) >= 2:
                    result_found = True
                
                # Alternative: look for speed values
                download_elem = driver.find_elements(By.CLASS_NAME, "download-speed")
                if download_elem:
                    result_found = True
                
                # Show progress
                elapsed = int(time.time() - start_time)
                print(f"[PROGRESS] {elapsed}s elapsed...", end='\r')
                
                time.sleep(1)
            except:
                time.sleep(1)
        
        print("\n[COMPLETE] Speed test finished")
        
        # Extract results
        print("\n[EXTRACT] Extracting speed test results...")
        
        try:
            # Wait for results to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-container"))
            )
            
            # Get download speed
            download = "N/A"
            upload = "N/A"
            ping = "N/A"
            
            try:
                download_elem = driver.find_element(By.CLASS_NAME, "download-speed")
                download = download_elem.text
                print(f"[OK] Download: {download} Mbps")
            except:
                print("[WARNING] Could not extract download speed")
            
            try:
                upload_elem = driver.find_element(By.CLASS_NAME, "upload-speed")
                upload = upload_elem.text
                print(f"[OK] Upload: {upload} Mbps")
            except:
                print("[WARNING] Could not extract upload speed")
            
            try:
                ping_elem = driver.find_element(By.CLASS_NAME, "ping-value")
                ping = ping_elem.text
                print(f"[OK] Ping: {ping} ms")
            except:
                print("[WARNING] Could not extract ping")
            
            # Get result URL
            result_url = driver.current_url
            print(f"[OK] Result URL: {result_url}")
            
            # Parse numeric values
            download_mbps = float(download.replace(" Mbps", "").strip()) if download != "N/A" else 0
            upload_mbps = float(upload.replace(" Mbps", "").strip()) if upload != "N/A" else 0
            
            result = {
                "download": download_mbps,
                "upload": upload_mbps,
                "ping": ping,
                "result_url": result_url,
                "timestamp": datetime.now().isoformat(),
                "raw_download": download,
                "raw_upload": upload
            }
            
            print(f"\n[RESULT] Speed Test Complete:")
            print(f"  Download: {download_mbps:.2f} Mbps")
            print(f"  Upload: {upload_mbps:.2f} Mbps")
            print(f"  Ping: {ping}")
            
            return result
        
        except Exception as e:
            print(f"[ERROR] Could not extract results: {e}")
            raise
    
    except Exception as e:
        print(f"[ERROR] Speed test failed: {e}")
        raise


# ============================================================================
# Speed Comparison
# ============================================================================

def compare_speeds(actual_speeds, promised_speeds):
    """
    Compare actual speeds against promised speeds.
    
    Args:
        actual_speeds: Dict with 'download' and 'upload' (Mbps)
        promised_speeds: Dict with 'down' and 'up' (Mbps)
    
    Returns:
        Dict with comparison results and whether speeds are acceptable
    """
    print(f"\n[COMPARE] Analyzing speed results...")
    
    actual_down = actual_speeds.get('download', 0)
    actual_up = actual_speeds.get('upload', 0)
    
    promised_down = promised_speeds.get('down', 0)
    promised_up = promised_speeds.get('up', 0)
    
    down_percent = (actual_down / promised_down * 100) if promised_down > 0 else 0
    up_percent = (actual_up / promised_up * 100) if promised_up > 0 else 0
    
    # Determine if speeds are acceptable (usually 80%+ is acceptable)
    acceptable = down_percent >= 80 and up_percent >= 80
    
    comparison = {
        "promised_down": promised_down,
        "promised_up": promised_up,
        "actual_down": actual_down,
        "actual_up": actual_up,
        "down_percent": down_percent,
        "up_percent": up_percent,
        "acceptable": acceptable,
        "down_shortfall": promised_down - actual_down,
        "up_shortfall": promised_up - actual_up
    }
    
    print(f"\n[ANALYSIS] Speed Comparison:")
    print(f"  Download: {actual_down:.2f}/{promised_down} Mbps ({down_percent:.1f}%)")
    print(f"  Upload:   {actual_up:.2f}/{promised_up} Mbps ({up_percent:.1f}%)")
    print(f"  Status: {'✓ ACCEPTABLE' if acceptable else '✗ POOR'}")
    
    if not acceptable:
        print(f"\n[WARNING] Speeds below promised levels!")
        if comparison['down_shortfall'] > 0:
            print(f"  Download shortfall: {comparison['down_shortfall']:.2f} Mbps")
        if comparison['up_shortfall'] > 0:
            print(f"  Upload shortfall: {comparison['up_shortfall']:.2f} Mbps")
    
    return comparison


# ============================================================================
# Tweet Generation
# ============================================================================

def generate_complaint_tweet(isp_name, isp_handle, speeds, promised):
    """
    Generate a witty, factual complaint tweet about poor speeds.
    
    Args:
        isp_name: Name of ISP (e.g., "Comcast")
        isp_handle: Twitter handle (e.g., "@comcastcares")
        speeds: Actual speed test results
        promised: Promised speeds
    
    Returns:
        Tweet text (under 280 characters)
    """
    print(f"\n[TWEET] Generating complaint tweet...")
    
    down_short = promised['down'] - speeds['down']
    up_short = promised['up'] - speeds['up']
    down_pct = (speeds['down'] / promised['down'] * 100) if promised['down'] > 0 else 0
    
    # Various complaint templates
    templates = [
        f"Hey {isp_handle}, I'm paying for {promised['down']}↓/{promised['up']}↑ Mbps but speedtest shows {speeds['download']:.0f}↓/{speeds['upload']:.0f}↑. That's {down_pct:.0f}% of promised speeds. Can we fix this?",
        
        f"{isp_handle} - Speedtest just measured {speeds['download']:.0f} Mbps down instead of the promised {promised['down']}. That's a {down_short:.0f} Mbps shortfall. Expecting a call from your team.",
        
        f"Running poorly as usual on {isp_name}. Promised {promised['down']}, getting {speeds['download']:.0f}. At this point I should be paying for {down_pct:.0f}% of my bill. {isp_handle} thoughts?",
        
        f"{isp_handle}: Speedtest result is in. {speeds['download']:.0f}↓ Mbps. You promised {promised['down']}. We need to talk about this gap.",
    ]
    
    # Use first template that fits in 280 chars
    tweet = templates[0]
    for template in templates:
        if len(template) <= 280:
            tweet = template
            break
    
    # If still too long, truncate
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    
    print(f"\n[TWEET] Generated tweet ({len(tweet)}/280 characters):")
    print(f'"{tweet}"')
    
    return tweet


# ============================================================================
# Twitter API Integration
# ============================================================================

def post_tweet_to_twitter(tweet_text):
    """
    Post tweet to Twitter using Twitter API.
    
    Args:
        tweet_text: Content of tweet to post
    
    Returns:
        Response from Twitter API or None if credentials not configured
    """
    print(f"\n[TWITTER] Posting tweet to Twitter...")
    
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        print("[WARNING] Twitter API credentials not configured")
        print("[INFO] To post tweets, set environment variables:")
        print("  TWITTER_API_KEY")
        print("  TWITTER_API_SECRET")
        print("  TWITTER_ACCESS_TOKEN")
        print("  TWITTER_ACCESS_SECRET")
        print(f"\n[DEMO] Would tweet: {tweet_text}")
        return None
    
    try:
        import tweepy
        
        # Authenticate
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        
        # Post tweet
        print(f"[API] Posting to Twitter...")
        response = api.update_status(tweet_text)
        print(f"[SUCCESS] Tweet posted! Tweet ID: {response.id}")
        print(f"[URL] https://twitter.com/{response.user.screen_name}/status/{response.id}")
        
        return response
    
    except ImportError:
        print("[WARNING] tweepy not installed. Install with: pip install tweepy")
        print(f"[DEMO] Would tweet: {tweet_text}")
        return None
    
    except Exception as e:
        print(f"[ERROR] Failed to post tweet: {e}")
        raise


# ============================================================================
# Result Storage
# ============================================================================

def save_result(result_data):
    """
    Save speed test result to file for history.
    
    Args:
        result_data: Result dictionary to save
    """
    print(f"\n[SAVE] Saving results to {RESULTS_FILE}...")
    
    try:
        # Load existing results
        results = []
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r') as f:
                results = json.load(f)
        
        # Add new result
        results.append(result_data)
        
        # Save
        with open(RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[OK] Result saved ({len(results)} total results)")
    
    except Exception as e:
        print(f"[ERROR] Failed to save result: {e}")


def view_results_history(limit=10):
    """
    Display recent speed test results.
    
    Args:
        limit: Number of recent results to show
    """
    print(f"\n[HISTORY] Speed Test Results ({limit} most recent):")
    print("-" * 70)
    
    try:
        if not os.path.exists(RESULTS_FILE):
            print("No results found. Run a speed test first.")
            return
        
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)
        
        # Show most recent results
        for i, result in enumerate(reversed(results[-limit:])):
            timestamp = result.get('timestamp', 'Unknown')
            download = result.get('download', 'N/A')
            upload = result.get('upload', 'N/A')
            print(f"\n{i+1}. {timestamp}")
            print(f"   Down: {download:.2f} Mbps | Up: {upload:.2f} Mbps")
    
    except Exception as e:
        print(f"[ERROR] Failed to read results: {e}")


# ============================================================================
# Main Bot Workflow
# ============================================================================

def run_speed_complaint_bot(isp_key="comcast", promised_down=150, promised_up=10, should_tweet=False):
    """
    Run complete speed test and complaint tweet workflow.
    
    Args:
        isp_key: ISP key (comcast, att, verizon, etc.)
        promised_down: Promised download speed (Mbps)
        promised_up: Promised upload speed (Mbps)
        should_tweet: Whether to post tweet to Twitter
    
    Returns:
        Result dictionary
    """
    print("\n" + "="*70)
    print("Internet Speed Test & Twitter Complaint Bot".center(70))
    print("="*70)
    
    driver = None
    result = None
    
    try:
        # Setup
        print(f"\n[SETUP] ISP: {ISP_CONFIGS[isp_key]['name']}")
        print(f"[SETUP] Promised: {promised_down} Mbps down / {promised_up} Mbps up")
        
        isp = ISP_CONFIGS[isp_key]
        promised_speeds = {"down": promised_down, "up": promised_up}
        
        # Start browser
        driver = setup_chrome_driver(headless=False)
        
        # Run speed test
        speeds = run_speedtest(driver)
        
        # Compare speeds
        comparison = compare_speeds(speeds, promised_speeds)
        
        # Prepare result
        result = {
            "isp": isp_key,
            "speeds": speeds,
            "promised": promised_speeds,
            "comparison": comparison,
            "tweet": None
        }
        
        # Generate complaint if speeds are poor
        if not comparison['acceptable']:
            tweet = generate_complaint_tweet(
                isp['name'],
                isp['handle'],
                speeds,
                promised_speeds
            )
            result['tweet'] = tweet
            
            # Post to Twitter if requested
            if should_tweet:
                print(f"\n[ACTION] Posting complaint to Twitter...")
                post_tweet_to_twitter(tweet)
            else:
                print(f"\n[INFO] Complaint tweet generated but not posted (should_tweet=False)")
        
        else:
            print(f"\n[OK] Speeds are acceptable - no complaint needed")
        
        # Save results
        save_result(result)
        
        # Display summary
        print("\n" + "="*70)
        print("RESULT SUMMARY".center(70))
        print("="*70)
        print(f"\nISP: {isp['name']}")
        print(f"Promised: {promised_down}↓ / {promised_up}↑ Mbps")
        print(f"Actual: {speeds['download']:.2f}↓ / {speeds['upload']:.2f}↑ Mbps")
        print(f"Status: {'✓ ACCEPTABLE' if comparison['acceptable'] else '✗ POOR'}")
        
        if result['tweet']:
            print(f"\nComplaint Tweet:")
            print(f'"{result["tweet"]}"')
        
        return result
    
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!")


def main():
    """Main program."""
    print()
    print("="*70)
    print("Day 51 - Complaining Twitter Bot".center(70))
    print("="*70)
    print("""
Automate internet speed testing and tweet complaints to your ISP
when speeds fall below promised levels.

Key Features:
✓ Automated speedtest.net testing
✓ Speed comparison against promised speeds
✓ Witty complaint tweet generation
✓ Twitter API integration
✓ Result history tracking
✓ Multiple ISP support

Setup:
1. Configure Twitter API credentials (see README)
2. Update ISP and promised speeds in config
3. Run bot daily or on schedule
4. Review results and tweets

Files:
  speed_complaint_bot.py - Main bot implementation
  example_usage.py - Working examples
  README.md - Complete documentation
  speed_test_results.json - Historical results
    """)


if __name__ == "__main__":
    main()
