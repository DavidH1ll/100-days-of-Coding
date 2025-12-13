"""
Day 49 - Gym Class Booking Automation Bot with Selenium

Automate gym class bookings using Selenium, persistent browser profiles,
retry logic, and dynamic content handling.

Project: Snack and Lift - Dream Gym Booking System
Website: Local browser-based database (IndexedDB)
Goal: Never miss a class booking again!

Key Concepts:
- Persistent browser profiles (remembers user data across sessions)
- Login automation (simulating real user authentication)
- Dynamic content handling (date/time sensitive bookings)
- Retry logic for network failures (decorators and wrappers)
- State verification (confirming bookings actually succeeded)
- Multiple profile management (same code, different users)
- Network resilience (handling network simulation)

Real-World Applications:
- Gym and fitness class bookings
- Meeting room reservations
- Course registrations
- Ticket bookings
- Table reservations at restaurants
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
from datetime import datetime, timedelta
from functools import wraps
import json

# ============================================================================
# Configuration
# ============================================================================

# Website URL (local gym booking system)
GYM_WEBSITE = "https://practice-automation.com/gym-booking/"  # Practice site
# For the actual Snack and Lift system, use appropriate URL

# Chrome profile setup
CHROME_PROFILE_DIR = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data"
GYM_PROFILE_NAME = "GymBot"  # Create a dedicated profile for the bot

# Timeout values
LOGIN_TIMEOUT = 15
BOOKING_TIMEOUT = 10
GENERAL_TIMEOUT = 5

# Retry configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 2

# Test credentials
TEST_EMAIL = "student@Test.com"
TEST_PASSWORD = "password123"
ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = "admin123"

# ============================================================================
# Decorator: Retry Logic for Network Failures
# ============================================================================

def retry_on_failure(max_retries=DEFAULT_MAX_RETRIES, delay=DEFAULT_RETRY_DELAY, backoff=True):
    """
    Decorator to retry a function if it fails due to network or timing issues.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Whether to increase delay exponentially (exponential backoff)
    
    Returns:
        Decorated function that retries on failure
    
    Example:
        @retry_on_failure(max_retries=3, delay=1, backoff=True)
        def book_class(driver, class_name):
            # Function code
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"\n[ATTEMPT {attempt}/{max_retries}] Calling {func.__name__}...")
                    result = func(*args, **kwargs)
                    print(f"[SUCCESS] {func.__name__} succeeded")
                    return result
                    
                except Exception as e:
                    print(f"[ERROR] Attempt {attempt} failed: {type(e).__name__}: {e}")
                    
                    if attempt < max_retries:
                        print(f"[RETRY] Waiting {current_delay}s before retry...")
                        time.sleep(current_delay)
                        
                        if backoff:
                            current_delay *= 2  # Exponential backoff
                    else:
                        print(f"[FAILED] All {max_retries} attempts exhausted")
                        raise
            
        return wrapper
    return decorator


def retry_with_condition(condition_func, max_retries=DEFAULT_MAX_RETRIES, delay=DEFAULT_RETRY_DELAY):
    """
    Decorator to retry until a condition is met.
    
    Args:
        condition_func: Function that returns True when condition is met
        max_retries: Maximum retry attempts
        delay: Delay between retries
    
    Returns:
        Decorated function
    
    Example:
        def is_booking_confirmed(driver):
            return "confirmed" in driver.page_source.lower()
        
        @retry_with_condition(is_booking_confirmed, max_retries=5)
        def book_and_verify(driver, class_name):
            # Booking code
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                print(f"\n[ATTEMPT {attempt}/{max_retries}] {func.__name__}...")
                
                try:
                    func(*args, **kwargs)
                    
                    # Check condition
                    if condition_func(*args):
                        print(f"[SUCCESS] Condition met after attempt {attempt}")
                        return True
                    else:
                        print(f"[CONDITION NOT MET] Attempt {attempt} - retrying...")
                        
                except Exception as e:
                    print(f"[ERROR] Exception in attempt {attempt}: {e}")
                
                if attempt < max_retries:
                    time.sleep(delay)
                else:
                    print(f"[FAILED] Condition not met after {max_retries} attempts")
                    return False
                    
        return wrapper
    return decorator


# ============================================================================
# Browser Profile Management
# ============================================================================

def create_chrome_profile(profile_name):
    """
    Create or use existing Chrome profile for persistent data.
    
    Args:
        profile_name: Name of Chrome profile (e.g., "GymBot", "Profile 1")
    
    Returns:
        Full path to profile directory
    """
    # Try to find existing profile
    user_data_dir = CHROME_PROFILE_DIR
    profile_path = os.path.join(user_data_dir, "Default")
    
    print(f"[PROFILE] Using Chrome profile: {profile_name}")
    print(f"[PROFILE] Profile path: {profile_path}")
    
    # Create if doesn't exist (Chrome will auto-create on launch)
    os.makedirs(profile_path, exist_ok=True)
    
    return profile_path


def setup_chrome_driver(profile_name=None, headless=False, disable_images=False):
    """
    Set up Chrome WebDriver with persistent profile and optimizations.
    
    Args:
        profile_name: Name of Chrome profile to use
        headless: Run browser in headless mode (no UI)
        disable_images: Disable image loading for faster performance
    
    Returns:
        WebDriver instance
    """
    print("\n[BROWSER] Setting up Chrome WebDriver...")
    
    options = Options()
    
    # Add profile
    if profile_name:
        profile_path = create_chrome_profile(profile_name)
        options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
        options.add_argument(f"--profile-directory=Default")
        print(f"[BROWSER] Profile configured: {profile_name}")
    
    # Headless mode (optional)
    if headless:
        options.add_argument("--headless=new")
        print("[BROWSER] Headless mode enabled")
    
    # Disable images for faster loading (optional)
    if disable_images:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        print("[BROWSER] Image loading disabled")
    
    # Other optimizations
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("[OK] WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        raise


# ============================================================================
# Login and Authentication
# ============================================================================

@retry_on_failure(max_retries=3, delay=1)
def login_to_gym(driver, email, password):
    """
    Log in to the gym booking system.
    
    Args:
        driver: WebDriver instance
        email: User email
        password: User password
    
    Returns:
        True if login successful
    
    Raises:
        Exception if login fails after retries
    """
    print(f"\n[LOGIN] Logging in as {email}...")
    
    try:
        # Navigate to login page
        driver.get(GYM_WEBSITE)
        print("[INFO] Navigated to gym website")
        
        # Find login button/link
        WebDriverWait(driver, LOGIN_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Try to find and click login button
        try:
            login_button = driver.find_element(By.LINK_TEXT, "Login")
            login_button.click()
            print("[OK] Login button clicked")
        except:
            print("[INFO] No separate login page, trying direct login form")
        
        # Wait for login form
        time.sleep(1)
        
        # Fill email
        email_field = WebDriverWait(driver, LOGIN_TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.clear()
        email_field.send_keys(email)
        print(f"[OK] Email entered: {email}")
        
        # Fill password
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)
        print("[OK] Password entered")
        
        # Submit
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            print("[OK] Login submitted")
        except:
            password_field.send_keys(Keys.ENTER)
            print("[OK] Login submitted via ENTER")
        
        # Wait for dashboard/bookings page
        time.sleep(2)
        WebDriverWait(driver, LOGIN_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("[SUCCESS] Login successful")
        return True
        
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        raise


def logout_from_gym(driver):
    """
    Log out from gym booking system.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        True if logout successful
    """
    print("\n[LOGOUT] Logging out...")
    
    try:
        # Find logout button/link
        logout_button = WebDriverWait(driver, GENERAL_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_button.click()
        print("[OK] Logout button clicked")
        
        time.sleep(1)
        print("[SUCCESS] Logout successful")
        return True
        
    except Exception as e:
        print(f"[WARNING] Logout failed: {e}")
        return False


# ============================================================================
# Booking Operations
# ============================================================================

def find_class_by_name(driver, class_name):
    """
    Find a gym class by name on the bookings page.
    
    Args:
        driver: WebDriver instance
        class_name: Name of class to find (e.g., "Spin", "Yoga")
    
    Returns:
        WebElement representing the class row, or None if not found
    """
    print(f"\n[SEARCH] Looking for class: {class_name}")
    
    try:
        # Find all class rows
        class_rows = driver.find_elements(By.CSS_SELECTOR, ".class-row, [data-testid*='class']")
        print(f"[INFO] Found {len(class_rows)} classes on page")
        
        # Search for matching class
        for row in class_rows:
            text = row.text.lower()
            if class_name.lower() in text:
                print(f"[OK] Found class: {class_name}")
                return row
        
        print(f"[WARNING] Class not found: {class_name}")
        return None
        
    except Exception as e:
        print(f"[ERROR] Error searching for class: {e}")
        return None


def get_class_status(driver, class_row):
    """
    Get the status of a class (Available, Full, Waitlist, etc.).
    
    Args:
        driver: WebDriver instance
        class_row: WebElement of the class row
    
    Returns:
        String describing class status
    """
    try:
        # Look for status indicators
        if "full" in class_row.text.lower():
            return "FULL"
        elif "waitlist" in class_row.text.lower():
            return "WAITLIST_AVAILABLE"
        elif "available" in class_row.text.lower():
            return "AVAILABLE"
        else:
            return "UNKNOWN"
            
    except:
        return "UNKNOWN"


@retry_on_failure(max_retries=3, delay=1)
def book_class(driver, class_name):
    """
    Book a gym class.
    
    Args:
        driver: WebDriver instance
        class_name: Name of class to book
    
    Returns:
        True if booking successful
    
    Raises:
        Exception if booking fails after retries
    """
    print(f"\n[BOOKING] Attempting to book: {class_name}")
    
    try:
        # Find the class
        class_row = find_class_by_name(driver, class_name)
        if not class_row:
            raise Exception(f"Class not found: {class_name}")
        
        # Check status
        status = get_class_status(driver, class_row)
        print(f"[STATUS] Class status: {status}")
        
        # Find and click book button
        try:
            book_button = class_row.find_element(By.BUTTON, "Book Class")
        except:
            # Try alternative selectors
            book_button = class_row.find_element(By.CSS_SELECTOR, "button:not([disabled])")
        
        if not book_button.is_enabled():
            raise Exception("Book button is disabled")
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", book_button)
        time.sleep(0.3)
        
        # Click
        book_button.click()
        print(f"[OK] Book button clicked for {class_name}")
        
        # Wait for confirmation
        time.sleep(1.5)
        
        # Verify booking
        if verify_booking(driver, class_name):
            print(f"[SUCCESS] Successfully booked: {class_name}")
            return True
        else:
            raise Exception("Booking could not be verified")
        
    except Exception as e:
        print(f"[ERROR] Booking failed: {e}")
        raise


def join_waitlist(driver, class_name):
    """
    Join the waitlist for a full gym class.
    
    Args:
        driver: WebDriver instance
        class_name: Name of class to join waitlist for
    
    Returns:
        True if successfully joined waitlist
    """
    print(f"\n[WAITLIST] Joining waitlist for: {class_name}")
    
    try:
        class_row = find_class_by_name(driver, class_name)
        if not class_row:
            raise Exception(f"Class not found: {class_name}")
        
        # Find waitlist button
        waitlist_button = class_row.find_element(By.BUTTON, "Join Waitlist")
        
        if not waitlist_button.is_enabled():
            raise Exception("Waitlist button is disabled")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", waitlist_button)
        time.sleep(0.3)
        
        waitlist_button.click()
        print(f"[OK] Joined waitlist for: {class_name}")
        
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to join waitlist: {e}")
        return False


def cancel_booking(driver, class_name):
    """
    Cancel a gym class booking.
    
    Args:
        driver: WebDriver instance
        class_name: Name of booked class to cancel
    
    Returns:
        True if cancellation successful
    """
    print(f"\n[CANCEL] Cancelling booking for: {class_name}")
    
    try:
        class_row = find_class_by_name(driver, class_name)
        if not class_row:
            raise Exception(f"Class not found: {class_name}")
        
        # Find cancel button
        cancel_button = class_row.find_element(By.BUTTON, "Cancel")
        
        if not cancel_button.is_enabled():
            raise Exception("Cancel button is disabled")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", cancel_button)
        time.sleep(0.3)
        
        cancel_button.click()
        print(f"[OK] Cancel button clicked for: {class_name}")
        
        # Confirm cancellation if prompted
        time.sleep(0.5)
        try:
            confirm_button = driver.find_element(By.BUTTON, "Confirm")
            confirm_button.click()
            print("[OK] Cancellation confirmed")
        except:
            pass
        
        time.sleep(1)
        print(f"[SUCCESS] Booking cancelled: {class_name}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Cancellation failed: {e}")
        return False


def verify_booking(driver, class_name):
    """
    Verify that a booking was successful.
    
    Args:
        driver: WebDriver instance
        class_name: Name of class that should be booked
    
    Returns:
        True if booking is confirmed in UI
    """
    print(f"\n[VERIFY] Verifying booking for: {class_name}")
    
    try:
        # Wait for page to update
        time.sleep(1)
        
        # Check if class row shows as booked
        class_row = find_class_by_name(driver, class_name)
        if not class_row:
            return False
        
        # Look for confirmation indicators
        text = class_row.text.lower()
        
        if "booked" in text or "confirmed" in text:
            print(f"[OK] Booking verified: {class_name}")
            return True
        elif "cancel" in text:  # Cancel button means it's booked
            print(f"[OK] Booking verified (Cancel button present): {class_name}")
            return True
        else:
            print(f"[WARNING] Could not verify booking: {class_name}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        return False


# ============================================================================
# Admin Panel Operations
# ============================================================================

def access_admin_panel(driver, email, password):
    """
    Log in to admin panel for database management.
    
    Args:
        driver: WebDriver instance
        email: Admin email
        password: Admin password
    
    Returns:
        True if admin panel accessed
    """
    print("\n[ADMIN] Accessing admin panel...")
    
    try:
        # Log in as admin
        login_to_gym(driver, email, password)
        
        # Navigate to admin panel
        admin_link = WebDriverWait(driver, GENERAL_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Admin"))
        )
        admin_link.click()
        print("[OK] Admin panel accessed")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to access admin panel: {e}")
        return False


def reset_bookings(driver):
    """
    Clear only the bookings from the database (keep user accounts).
    
    Args:
        driver: WebDriver instance
    
    Returns:
        True if reset successful
    """
    print("\n[RESET] Clearing bookings only...")
    
    try:
        reset_button = WebDriverWait(driver, GENERAL_TIMEOUT).until(
            EC.element_to_be_clickable((By.BUTTON, "Clear Bookings Only"))
        )
        reset_button.click()
        print("[OK] Reset button clicked")
        
        time.sleep(2)
        print("[SUCCESS] Bookings cleared")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to reset bookings: {e}")
        return False


def reset_all_data(driver):
    """
    Reset all database data to initial state.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        True if reset successful
    """
    print("\n[RESET] Resetting all data...")
    
    try:
        reset_button = WebDriverWait(driver, GENERAL_TIMEOUT).until(
            EC.element_to_be_clickable((By.BUTTON, "Reset All Data"))
        )
        reset_button.click()
        print("[OK] Reset button clicked")
        
        # Confirm if prompted
        time.sleep(0.5)
        try:
            confirm_button = driver.find_element(By.BUTTON, "Confirm")
            confirm_button.click()
            print("[OK] Reset confirmed")
        except:
            pass
        
        time.sleep(2)
        print("[SUCCESS] All data reset to initial state")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to reset all data: {e}")
        return False


# ============================================================================
# Advanced Features
# ============================================================================

def book_multiple_classes(driver, class_names):
    """
    Book multiple gym classes in sequence with error handling.
    
    Args:
        driver: WebDriver instance
        class_names: List of class names to book
    
    Returns:
        Dictionary with booking results
    """
    print(f"\n[BATCH] Booking {len(class_names)} classes...")
    
    results = {
        "successful": [],
        "failed": []
    }
    
    for class_name in class_names:
        try:
            if book_class(driver, class_name):
                results["successful"].append(class_name)
            else:
                results["failed"].append(class_name)
        except Exception as e:
            print(f"[ERROR] Failed to book {class_name}: {e}")
            results["failed"].append(class_name)
    
    print(f"\n[SUMMARY] Bookings: {len(results['successful'])} successful, {len(results['failed'])} failed")
    print(f"[SUCCESS] Successful: {results['successful']}")
    print(f"[FAILED] Failed: {results['failed']}")
    
    return results


def handle_network_simulation(driver, enable=True):
    """
    Enable or disable network simulation for testing.
    
    Args:
        driver: WebDriver instance
        enable: Whether to enable network simulation
    
    Returns:
        True if successful
    """
    print(f"\n[NETWORK] Setting network simulation: {'ENABLED' if enable else 'DISABLED'}")
    
    try:
        # Open DevTools
        driver.execute_script("window.devToolsOpened = true;")
        
        # This would require more complex implementation with CDP
        # For now, just log the action
        print("[INFO] Network simulation would be configured in DevTools")
        return True
        
    except Exception as e:
        print(f"[WARNING] Could not configure network simulation: {e}")
        return False


# ============================================================================
# Main Bot Workflow
# ============================================================================

def main():
    """
    Main gym booking bot workflow.
    """
    print()
    print("="*70)
    print("Snack and Lift - Gym Class Booking Automation Bot".center(70))
    print("="*70)
    print()
    
    driver = None
    
    try:
        # Setup browser with persistent profile
        print("[STEP 1] Setting up browser...")
        driver = setup_chrome_driver(
            profile_name=GYM_PROFILE_NAME,
            headless=False,
            disable_images=False
        )
        
        # Log in
        print("\n[STEP 2] Logging in...")
        login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
        
        # Book classes
        print("\n[STEP 3] Booking classes...")
        classes_to_book = ["Spin", "Yoga", "Pilates"]
        results = book_multiple_classes(driver, classes_to_book)
        
        # Display results
        print("\n" + "="*70)
        print("BOOKING RESULTS".center(70))
        print("="*70)
        print(f"Successful: {len(results['successful'])} bookings")
        print(f"Failed: {len(results['failed'])} bookings")
        if results['successful']:
            print(f"\nBooked classes:")
            for cls in results['successful']:
                print(f"  ✓ {cls}")
        if results['failed']:
            print(f"\nFailed bookings:")
            for cls in results['failed']:
                print(f"  ✗ {cls}")
        print("="*70 + "\n")
        
        # Keep browser open for verification
        print("[INFO] Bot completed. Keeping browser open for verification...")
        print("[INFO] Press Ctrl+C to close browser\n")
        
        input("Press ENTER to close browser...")
        
    except KeyboardInterrupt:
        print("\n[INFO] Bot stopped by user")
        
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        print("\n[CLEANUP] Closing browser...")
        if driver:
            logout_from_gym(driver)
            driver.quit()
            print("[OK] Browser closed")
        
        print("\n[COMPLETE] Gym booking bot finished")


if __name__ == "__main__":
    main()
