"""
Day 52 - Instagram Follower Bot
Automates following Instagram users based on target accounts

This bot implements the "follow similar audience" strategy:
1. Login to Instagram
2. Navigate to target account
3. Open followers list
4. Follow each follower with configurable delays
5. Track results and maintain history
"""

import time
import json
import os
from datetime import datetime
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

INSTAGRAM_URL = "https://www.instagram.com"
RESULTS_FILE = "follower_bot_results.json"

# Target accounts to harvest followers from
TARGET_ACCOUNTS = {
    "chefsteps": {
        "username": "chefsteps",
        "category": "cooking",
        "description": "Cooking and molecular gastronomy content"
    },
    "gordon_ramsay": {
        "username": "gordonramsay",
        "category": "cooking",
        "description": "Celebrity chef content"
    },
    "tasty": {
        "username": "tasty",
        "category": "food",
        "description": "Quick food recipes and videos"
    },
    "seriouseats": {
        "username": "seriouseats",
        "category": "food",
        "description": "Food news and recipes"
    },
    "babish": {
        "username": "bingingwithbabish",
        "category": "cooking",
        "description": "Recreating fictional foods"
    },
    "matcha_dna": {
        "username": "matcha_dna",
        "category": "beverages",
        "description": "Matcha and tea content"
    }
}

# Follow delays (seconds)
DELAYS = {
    "between_follows": 5,      # Delay between each follow
    "between_batches": 60,     # Delay between batches of 50
    "on_error": 10,            # Delay after error
    "page_load": 3,            # Page load wait time
}

# Rate limiting
BATCH_SIZE = 50             # Follows per batch before pause
BATCH_PAUSE = 60            # Seconds between batches
MAX_FOLLOWS_PER_SESSION = 300  # Max follows in one session
SMART_PAUSE_INTERVAL = 100  # Add random longer pause every N follows


# ============================================================================
# DECORATORS
# ============================================================================

def retry_on_failure(max_retries=3, delay=2, backoff=True):
    """
    Decorator to retry function on failure with exponential backoff.
    
    Args:
        max_retries: Number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Whether to use exponential backoff
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"[RETRY] Attempt {attempt + 1} failed: {str(e)[:50]}")
                        print(f"[WAIT] Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        if backoff:
                            current_delay *= 2
                    else:
                        print(f"[FAILED] Max retries reached for {func.__name__}")
            
            raise last_exception
        
        return wrapper
    return decorator


# ============================================================================
# BROWSER SETUP
# ============================================================================

def setup_chrome_driver(headless=False, profile_name="instagram_bot"):
    """
    Setup Chrome WebDriver with appropriate options.
    
    Args:
        headless: Run in headless mode (no UI)
        profile_name: Chrome profile name for persistence
    
    Returns:
        Configured WebDriver instance
    """
    print("[SETUP] Initializing Chrome WebDriver...")
    
    options = Options()
    
    # User profile for persistent login
    profile_path = os.path.expanduser(f"~\\AppData\\Local\\Google\\Chrome\\User Data\\{profile_name}")
    options.add_argument(f"user-data-dir={profile_path}")
    
    if headless:
        options.add_argument("--headless")
    
    # Additional options
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Disable notifications
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    
    try:
        driver = webdriver.Chrome(options=options)
        print("[OK] Chrome WebDriver initialized\n")
        return driver
    
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        raise


# ============================================================================
# AUTHENTICATION
# ============================================================================

@retry_on_failure(max_retries=3, delay=2)
def login_to_instagram(driver, username, password):
    """
    Login to Instagram.
    
    Args:
        driver: WebDriver instance
        username: Instagram username
        password: Instagram password
    
    Returns:
        True if login successful, False otherwise
    """
    print(f"[LOGIN] Logging in as {username}...")
    
    driver.get(f"{INSTAGRAM_URL}/accounts/login/")
    time.sleep(3)
    
    # Find and fill username field
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_field.clear()
    username_field.send_keys(username)
    print("[FIELD] Username entered")
    
    # Find and fill password field
    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(password)
    print("[FIELD] Password entered")
    
    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='button']")
    login_button.click()
    print("[CLICK] Login button clicked")
    
    # Wait for navigation to complete
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//svg[@aria-label='Home']"))
    )
    
    print("[OK] Successfully logged in\n")
    return True


def logout_from_instagram(driver):
    """Logout from Instagram."""
    try:
        print("[LOGOUT] Logging out...")
        
        # Click profile icon
        profile_icon = driver.find_element(By.XPATH, "//svg[@aria-label='Profile']/..")
        profile_icon.click()
        time.sleep(1)
        
        # Click logout button
        logout_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Log out')]"))
        )
        logout_button.click()
        
        time.sleep(2)
        print("[OK] Successfully logged out\n")
    
    except Exception as e:
        print(f"[WARN] Logout failed: {e}\n")


# ============================================================================
# NAVIGATION
# ============================================================================

@retry_on_failure(max_retries=3, delay=2)
def navigate_to_profile(driver, username):
    """
    Navigate to a specific Instagram profile.
    
    Args:
        driver: WebDriver instance
        username: Instagram username to navigate to
    
    Returns:
        True if successful
    """
    print(f"[NAV] Navigating to @{username}...")
    
    driver.get(f"{INSTAGRAM_URL}/{username}/")
    time.sleep(3)
    
    # Verify we're on the right profile
    profile_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//h1[contains(text(), '{username}')]"))
    )
    
    print(f"[OK] Successfully navigated to @{username}\n")
    return True


@retry_on_failure(max_retries=3, delay=2)
def open_followers_modal(driver):
    """
    Open the followers modal on a profile page.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        True if successful
    """
    print("[FOLLOWERS] Opening followers list...")
    
    # Find followers link/button
    followers_link_xpaths = [
        "//a[contains(@href, '/followers/')]",
        "//button[contains(text(), 'followers')]",
        "//span[contains(text(), 'followers')]/..",
    ]
    
    followers_element = None
    for xpath in followers_link_xpaths:
        try:
            followers_element = driver.find_element(By.XPATH, xpath)
            if followers_element:
                break
        except NoSuchElementException:
            continue
    
    if not followers_element:
        raise Exception("Could not find followers element")
    
    # Click followers
    driver.execute_script("arguments[0].click();", followers_element)
    time.sleep(2)
    
    # Wait for modal to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
    )
    
    print("[OK] Followers modal opened\n")
    return True


# ============================================================================
# FOLLOWER OPERATIONS
# ============================================================================

def get_follow_button(driver, follower_element):
    """
    Get the follow button for a follower in the modal.
    
    Args:
        driver: WebDriver instance
        follower_element: The follower element in modal
    
    Returns:
        Follow button element or None
    """
    try:
        # Look for button with "Follow" text
        follow_button = follower_element.find_element(
            By.XPATH,
            ".//button[contains(text(), 'Follow') or contains(text(), 'follow')]"
        )
        return follow_button
    
    except NoSuchElementException:
        return None


@retry_on_failure(max_retries=2, delay=1)
def follow_user(driver, follower_element, username):
    """
    Follow a specific user from followers list.
    
    Args:
        driver: WebDriver instance
        follower_element: The follower element
        username: Username to follow
    
    Returns:
        True if successfully followed
    """
    try:
        # Scroll follower into view
        driver.execute_script("arguments[0].scrollIntoView(true);", follower_element)
        time.sleep(0.5)
        
        # Get follow button
        follow_button = get_follow_button(driver, follower_element)
        
        if not follow_button:
            print(f"[SKIP] @{username} - Already following")
            return False
        
        # Click follow button
        driver.execute_script("arguments[0].click();", follow_button)
        
        print(f"[FOLLOW] Successfully followed @{username}")
        return True
    
    except StaleElementReferenceException:
        print(f"[ERROR] Stale element for @{username}, retrying...")
        raise
    
    except Exception as e:
        print(f"[ERROR] Failed to follow @{username}: {str(e)[:50]}")
        return False


def follow_users_from_followers(driver, count=50, start_index=0):
    """
    Follow users from the currently open followers modal.
    
    Args:
        driver: WebDriver instance
        count: Number of users to follow
        start_index: Index to start from
    
    Returns:
        Dictionary with follow statistics
    """
    print(f"[START] Beginning to follow {count} users...\n")
    
    stats = {
        "total_attempts": 0,
        "successful_follows": 0,
        "already_following": 0,
        "errors": 0,
        "usernames": []
    }
    
    # Get followers modal
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
    except TimeoutException:
        print("[ERROR] Could not find followers modal")
        return stats
    
    # Get followers list
    followers_list = modal.find_element(By.XPATH, ".//div[@role='presentation']")
    
    users_followed_in_batch = 0
    
    for i in range(start_index, start_index + count):
        try:
            # Get all follower buttons (refreshed each iteration)
            follower_buttons = followers_list.find_elements(
                By.XPATH,
                ".//*[contains(@class, 'follow-button-class')]/.."
            )
            
            # If buttons not found, try alternative approach
            if not follower_buttons:
                follower_buttons = driver.find_elements(
                    By.XPATH,
                    "//div[@role='dialog']//button[contains(text(), 'Follow')]/.."
                )
            
            if i >= len(follower_buttons):
                print(f"\n[END] Reached end of followers list at index {i}")
                break
            
            follower_element = follower_buttons[i]
            
            # Get username
            try:
                username_element = follower_element.find_element(
                    By.XPATH,
                    ".//*[@class='_ap3a']"  # Instagram username class
                )
                username = username_element.text
            except:
                username = f"User_{i}"
            
            stats["total_attempts"] += 1
            
            # Follow user
            followed = follow_user(driver, follower_element, username)
            
            if followed:
                stats["successful_follows"] += 1
                stats["usernames"].append(username)
                users_followed_in_batch += 1
            else:
                stats["already_following"] += 1
            
            # Delay between follows
            time.sleep(DELAYS["between_follows"])
            
            # Batch pause for rate limiting
            if users_followed_in_batch >= BATCH_SIZE:
                print(f"\n[PAUSE] Batch pause ({BATCH_PAUSE}s) to avoid rate limiting...")
                time.sleep(BATCH_PAUSE)
                users_followed_in_batch = 0
                print("[RESUME] Continuing...\n")
            
            # Check if we've reached max follows
            if stats["successful_follows"] >= MAX_FOLLOWS_PER_SESSION:
                print(f"\n[LIMIT] Reached max follows per session ({MAX_FOLLOWS_PER_SESSION})")
                break
        
        except ElementClickInterceptedException:
            print(f"[INTERCEPT] Click intercepted at index {i}, waiting...")
            time.sleep(DELAYS["on_error"])
            stats["errors"] += 1
        
        except Exception as e:
            print(f"[ERROR] Error at index {i}: {str(e)[:50]}")
            stats["errors"] += 1
            time.sleep(DELAYS["on_error"])
    
    return stats


# ============================================================================
# RESULT MANAGEMENT
# ============================================================================

def save_results(target_username, stats, isp_config=None):
    """
    Save follow results to JSON file.
    
    Args:
        target_username: Target account username
        stats: Statistics dictionary
        isp_config: ISP configuration (for compatibility)
    """
    try:
        # Load existing results
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r') as f:
                results = json.load(f)
        else:
            results = []
        
        # Create result entry
        result_entry = {
            "timestamp": datetime.now().isoformat(),
            "target_account": target_username,
            "follows": {
                "successful": stats["successful_follows"],
                "already_following": stats["already_following"],
                "total_attempts": stats["total_attempts"],
                "errors": stats["errors"]
            },
            "followed_users": stats["usernames"][:20]  # Store first 20 usernames
        }
        
        results.append(result_entry)
        
        # Save results
        with open(RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[SAVED] Results saved to {RESULTS_FILE}")
    
    except Exception as e:
        print(f"[ERROR] Failed to save results: {e}")


def view_results_history(limit=10):
    """
    Display follower bot results history.
    
    Args:
        limit: Number of recent results to display
    """
    if not os.path.exists(RESULTS_FILE):
        print("[INFO] No results history found")
        return
    
    try:
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)
        
        print("\n" + "="*70)
        print("Follower Bot Results History".center(70))
        print("="*70 + "\n")
        
        for result in results[-limit:]:
            print(f"Date: {result['timestamp']}")
            print(f"Target: @{result['target_account']}")
            print(f"  Followed: {result['follows']['successful']}")
            print(f"  Already Following: {result['follows']['already_following']}")
            print(f"  Attempts: {result['follows']['total_attempts']}")
            print(f"  Errors: {result['follows']['errors']}")
            print()
    
    except Exception as e:
        print(f"[ERROR] Failed to load results: {e}")


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def run_follower_bot(
    instagram_username,
    instagram_password,
    target_account,
    num_follows=50,
    headless=False
):
    """
    Main workflow: Login, navigate, and follow users.
    
    Args:
        instagram_username: Your Instagram username
        instagram_password: Your Instagram password
        target_account: Username of account to harvest followers from
        num_follows: Number of users to follow
        headless: Run in headless mode
    
    Returns:
        Dictionary with results
    """
    driver = None
    
    try:
        # Setup
        print("="*70)
        print("Instagram Follower Bot".center(70))
        print("="*70 + "\n")
        
        driver = setup_chrome_driver(headless=headless)
        
        # Login
        login_to_instagram(driver, instagram_username, instagram_password)
        
        # Navigate to target account
        navigate_to_profile(driver, target_account)
        
        # Open followers
        open_followers_modal(driver)
        
        # Follow users
        stats = follow_users_from_followers(driver, count=num_follows)
        
        # Save results
        save_results(target_account, stats)
        
        # Display results
        print("\n" + "="*70)
        print("Session Summary".center(70))
        print("="*70)
        print(f"Target Account: @{target_account}")
        print(f"Follows Successful: {stats['successful_follows']}")
        print(f"Already Following: {stats['already_following']}")
        print(f"Total Attempts: {stats['total_attempts']}")
        print(f"Errors: {stats['errors']}")
        print("="*70 + "\n")
        
        return stats
    
    except Exception as e:
        print(f"\n[FATAL] Bot failed: {e}")
        print("[INFO] Check your credentials and try again\n")
        raise
    
    finally:
        if driver:
            logout_from_instagram(driver)
            driver.quit()
            print("[CLEANUP] Browser closed\n")


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Instagram Follower Bot - Main Module".center(70))
    print("="*70 + "\n")
    
    print("""
This module provides the core Instagram follower bot functionality.

USAGE EXAMPLE:
──────────────────────────────────────────────────────────────────────

from instagram_follower_bot import run_follower_bot

result = run_follower_bot(
    instagram_username="your_username",
    instagram_password="your_password",
    target_account="chefsteps",
    num_follows=50,
    headless=False
)

CONFIGURATION:
──────────────────────────────────────────────────────────────────────

Supported Target Accounts:
""")
    
    for key, config in TARGET_ACCOUNTS.items():
        print(f"  • {config['username']:<20} - {config['description']}")
    
    print("""

Delays (configurable in DELAYS dict):
  • between_follows: 5 seconds (between each follow)
  • between_batches: 60 seconds (after 50 follows)
  • on_error: 10 seconds (after errors)
  • page_load: 3 seconds (for page loads)

Rate Limiting:
  • Batch size: 50 follows per batch
  • Max per session: 300 follows
  • Smart pauses between batches

For working examples, see example_usage.py
For detailed documentation, see README.md
    """)
