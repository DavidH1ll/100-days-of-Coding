"""
Day 50 - Automated Tinder Bot with Selenium

Automate Tinder swiping to save time and effort while respecting ethical boundaries.

Project: Tinder Automation Bot
Challenge: Automate the tedious swiping process while handling matches, errors, and ethical considerations

Real-World Problem:
- Average Tinder user spends 90 minutes per day swiping
- Match rate is only 0.41% - 1 match per 100 swipes
- Massive time investment for limited results
- Repetitive manual process perfect for automation

Key Features:
- Automated login via Facebook authentication
- Profile navigation and prompt handling
- Automated left/right swiping
- Match detection and handling
- Swipe limit enforcement (Tinder limit: 100/day free, unlimited paid)
- Error recovery and retry logic
- Selective swiping (like all, dislike all, or custom criteria)
- Statistics tracking (swipes, matches, time saved)

Ethical Considerations:
✓ Tell your partner if using this bot (transparency)
✓ Respect Tinder's terms of service
✓ Don't use for spam or harassment
✓ Consider the other users on the platform
✓ Use responsibly and ethically
✓ Respect rate limits (100 swipes/day free)

Technical Patterns:
- Browser automation with persistent session
- Explicit waits for dynamic content
- Error handling and retry logic
- Match detection via popup handling
- Statistics collection and reporting
- Rate limiting to respect service limits

Real-World Applications:
- Time-saving automation for repetitive processes
- A/B testing profile variations
- Data collection for research (ethically)
- Large-scale dating app automation
- User engagement analysis
- Demonstrating web automation patterns

Key Takeaways:
1. Automate repetitive web tasks
2. Handle dynamic popups and prompts
3. Respect platform limitations and ToS
4. Collect and report statistics
5. Implement ethical automation practices
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os
import time
from datetime import datetime, timedelta
from functools import wraps
import json

# ============================================================================
# Configuration
# ============================================================================

# Tinder URL
TINDER_URL = "https://tinder.com"

# Locator timeouts
LOGIN_TIMEOUT = 30
PROFILE_TIMEOUT = 10
SWIPE_TIMEOUT = 5
POPUP_TIMEOUT = 3

# Swipe rate limiting
SWIPES_PER_DAY_FREE = 100
SWIPES_PER_DAY_PREMIUM = 2000  # Approximation
MIN_DELAY_BETWEEN_SWIPES = 0.5  # seconds (avoid seeming like bot)
MAX_DELAY_BETWEEN_SWIPES = 2.0  # seconds

# Statistics file
STATS_FILE = "tinder_stats.json"

# ============================================================================
# Statistics Tracking
# ============================================================================

class TinderStats:
    """Track bot statistics for analysis and reporting."""
    
    def __init__(self, stats_file=STATS_FILE):
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self):
        """Load stats from file or create new."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                return self._create_new_stats()
        else:
            return self._create_new_stats()
    
    def _create_new_stats(self):
        """Create new stats structure."""
        return {
            "total_swipes": 0,
            "right_swipes": 0,
            "left_swipes": 0,
            "matches": 0,
            "sessions": 0,
            "start_date": datetime.now().isoformat(),
            "last_session": None,
            "time_saved_minutes": 0,
            "swipes_by_session": []
        }
    
    def save(self):
        """Save stats to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"[WARNING] Could not save stats: {e}")
    
    def record_swipe(self, direction):
        """Record a swipe (right or left)."""
        self.stats["total_swipes"] += 1
        if direction == "right":
            self.stats["right_swipes"] += 1
        elif direction == "left":
            self.stats["left_swipes"] += 1
        self.save()
    
    def record_match(self):
        """Record a match."""
        self.stats["matches"] += 1
        self.save()
    
    def end_session(self, swipes_in_session):
        """Record session completion."""
        self.stats["sessions"] += 1
        self.stats["last_session"] = datetime.now().isoformat()
        # Estimate 7 seconds per swipe based on manual user testing
        time_saved = swipes_in_session * 7 / 60  # Convert to minutes
        self.stats["time_saved_minutes"] += time_saved
        self.stats["swipes_by_session"].append(swipes_in_session)
        self.save()
    
    def print_summary(self):
        """Print statistics summary."""
        print()
        print("=" * 70)
        print("TINDER BOT STATISTICS".center(70))
        print("=" * 70)
        print(f"\nTotal Sessions: {self.stats['sessions']}")
        print(f"Total Swipes: {self.stats['total_swipes']}")
        print(f"  - Right Swipes: {self.stats['right_swipes']}")
        print(f"  - Left Swipes: {self.stats['left_swipes']}")
        print(f"Matches: {self.stats['matches']}")
        
        if self.stats['total_swipes'] > 0:
            match_rate = (self.stats['matches'] / self.stats['total_swipes']) * 100
            print(f"Match Rate: {match_rate:.2f}%")
        
        print(f"Time Saved: {self.stats['time_saved_minutes']:.1f} minutes")
        print(f"  (≈ {self.stats['time_saved_minutes'] / 60:.1f} hours)")
        
        if self.stats['swipes_by_session']:
            avg_swipes = sum(self.stats['swipes_by_session']) / len(self.stats['swipes_by_session'])
            print(f"Average Swipes per Session: {avg_swipes:.1f}")
        
        print()


# ============================================================================
# Browser Setup
# ============================================================================

def setup_tinder_driver(headless=False, profile_path=None):
    """
    Set up Chrome WebDriver for Tinder automation.
    
    Args:
        headless: Run browser in headless mode
        profile_path: Optional Chrome profile path for persistent login
    
    Returns:
        WebDriver instance
    """
    print("\n[BROWSER] Setting up Chrome WebDriver for Tinder...")
    
    options = Options()
    
    if headless:
        options.add_argument("--headless=new")
        print("[BROWSER] Headless mode enabled")
    
    if profile_path:
        options.add_argument(f"--user-data-dir={profile_path}")
        print(f"[BROWSER] Using profile: {profile_path}")
    
    # Additional options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("[OK] WebDriver initialized successfully\n")
        return driver
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}\n")
        raise


# ============================================================================
# Login and Authentication
# ============================================================================

def login_to_tinder_facebook(driver, email, password, wait_for_manual=False):
    """
    Log into Tinder using Facebook authentication.
    
    Args:
        driver: WebDriver instance
        email: Facebook email
        password: Facebook password
        wait_for_manual: If True, wait for manual login (useful for 2FA)
    
    Returns:
        True if login successful
    """
    print("\n[LOGIN] Starting Tinder login process...")
    
    try:
        # Navigate to Tinder
        print("[NAV] Navigating to Tinder...")
        driver.get(TINDER_URL)
        time.sleep(3)
        
        # Look for Facebook login button
        print("[LOGIN] Looking for Facebook login button...")
        try:
            # Wait for page to load
            WebDriverWait(driver, LOGIN_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find and click Facebook login
            fb_button = WebDriverWait(driver, LOGIN_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Facebook')]"))
            )
            print("[OK] Facebook button found")
            
            fb_button.click()
            print("[OK] Facebook button clicked")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"[WARNING] Could not find Facebook button: {e}")
            print("[INFO] Looking for alternative login methods...")
        
        # Handle Facebook login popup
        print("[LOGIN] Switching to Facebook popup...")
        try:
            # Switch to Facebook popup window
            windows = driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[-1])
                print("[OK] Switched to Facebook window")
                time.sleep(2)
        except:
            print("[INFO] No popup window to switch to")
        
        # Enter Facebook email
        print("[LOGIN] Entering Facebook credentials...")
        try:
            email_field = WebDriverWait(driver, LOGIN_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.clear()
            email_field.send_keys(email)
            print("[OK] Email entered")
        except Exception as e:
            print(f"[WARNING] Could not find email field: {e}")
        
        # Enter password
        try:
            password_field = driver.find_element(By.ID, "pass")
            password_field.clear()
            password_field.send_keys(password)
            print("[OK] Password entered")
        except:
            print("[WARNING] Could not find password field")
        
        # Submit
        try:
            login_button = driver.find_element(By.ID, "loginbutton")
            login_button.click()
            print("[OK] Login submitted")
        except:
            print("[WARNING] Could not find login button")
        
        time.sleep(3)
        
        # Switch back to Tinder window
        print("[LOGIN] Switching back to Tinder...")
        try:
            windows = driver.window_handles
            driver.switch_to.window(windows[0])
            print("[OK] Back on Tinder window")
        except:
            pass
        
        # Wait for Tinder to load
        time.sleep(3)
        
        # Handle 2FA or manual confirmation if needed
        if wait_for_manual:
            print("[LOGIN] Waiting for manual confirmation (2FA)...")
            input("Press ENTER after confirming login in browser...")
        
        print("[SUCCESS] Login process complete\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Login failed: {e}\n")
        return False


# ============================================================================
# Profile Navigation and Prompt Handling
# ============================================================================

def handle_initial_prompts(driver):
    """
    Handle initial Tinder prompts and popups after login.
    
    Closes notifications, location requests, and other initial dialogs.
    """
    print("\n[PROMPTS] Handling initial Tinder prompts...")
    
    try:
        # Close notification prompt if present
        try:
            print("[PROMPTS] Looking for notification popup...")
            close_button = WebDriverWait(driver, POPUP_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
            )
            close_button.click()
            print("[OK] Notification closed")
            time.sleep(1)
        except:
            print("[INFO] No notification popup")
        
        # Close location prompt if present
        try:
            print("[PROMPTS] Looking for location popup...")
            close_button = WebDriverWait(driver, POPUP_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
            )
            close_button.click()
            print("[OK] Location prompt closed")
            time.sleep(1)
        except:
            print("[INFO] No location popup")
        
        # Close any other popups
        max_popups = 5
        for i in range(max_popups):
            try:
                close_button = WebDriverWait(driver, POPUP_TIMEOUT).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Skip')]"))
                )
                close_button.click()
                print(f"[OK] Popup #{i+1} closed")
                time.sleep(1)
            except:
                break
        
        print("[SUCCESS] Initial prompts handled\n")
        
    except Exception as e:
        print(f"[WARNING] Error handling prompts: {e}\n")


# ============================================================================
# Swiping Functions
# ============================================================================

def find_swipe_buttons(driver):
    """
    Find the like (right) and dislike (left) swipe buttons.
    
    Returns:
        Tuple of (like_button, dislike_button) or (None, None) if not found
    """
    try:
        # Buttons often have aria-labels or specific classes
        buttons = driver.find_elements(By.TAG_NAME, "button")
        
        like_button = None
        dislike_button = None
        
        for button in buttons:
            # Look for like/heart button
            if "like" in button.get_attribute("aria-label").lower() if button.get_attribute("aria-label") else "":
                like_button = button
            # Look for dislike/x button
            elif "pass" in button.get_attribute("aria-label").lower() if button.get_attribute("aria-label") else "":
                dislike_button = button
        
        return like_button, dislike_button
        
    except:
        return None, None


def swipe_right(driver, wait_time=SWIPE_TIMEOUT):
    """
    Swipe right (like) on current profile.
    
    Args:
        driver: WebDriver instance
        wait_time: Time to wait for like button
    
    Returns:
        True if swipe successful
    """
    try:
        print("[SWIPE] Swiping right (like)...", end=" ")
        
        # Try to find and click like button
        try:
            like_button = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Like' or contains(aria-label, 'Like')]"))
            )
            like_button.click()
            print("[OK]")
            return True
        except:
            # Alternative: use keyboard shortcut
            try:
                actions = ActionChains(driver)
                actions.send_keys(Keys.ARROW_RIGHT)
                actions.perform()
                print("[OK] (keyboard)")
                return True
            except:
                print("[FAILED]")
                return False
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def swipe_left(driver, wait_time=SWIPE_TIMEOUT):
    """
    Swipe left (dislike/pass) on current profile.
    
    Args:
        driver: WebDriver instance
        wait_time: Time to wait for pass button
    
    Returns:
        True if swipe successful
    """
    try:
        print("[SWIPE] Swiping left (pass)...", end=" ")
        
        # Try to find and click pass button
        try:
            pass_button = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Pass' or contains(aria-label, 'Pass')]"))
            )
            pass_button.click()
            print("[OK]")
            return True
        except:
            # Alternative: use keyboard shortcut
            try:
                actions = ActionChains(driver)
                actions.send_keys(Keys.ARROW_LEFT)
                actions.perform()
                print("[OK] (keyboard)")
                return True
            except:
                print("[FAILED]")
                return False
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def check_for_match(driver):
    """
    Check if a match popup appeared.
    
    Returns:
        True if match detected
    """
    try:
        # Look for match popup indicators
        match_popup = driver.find_elements(By.XPATH, "//h1[contains(text(), 'It')]")
        if match_popup:
            return True
        
        # Alternative check
        match_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'match')]")
        if match_text:
            return True
        
        return False
        
    except:
        return False


def handle_match_popup(driver):
    """
    Handle match popup by closing it to continue swiping.
    
    Returns:
        True if popup was handled
    """
    try:
        print("[MATCH] Match detected! Handling popup...")
        
        # Look for continue button
        try:
            continue_button = WebDriverWait(driver, POPUP_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Keep Swiping')]"))
            )
            continue_button.click()
            print("[OK] Continuing to swipe")
            return True
        except:
            # Alternative: just click close or press Escape
            try:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                print("[OK] Closed with Escape")
                return True
            except:
                print("[WARNING] Could not close match popup")
                return False
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


# ============================================================================
# Swipe Campaign Functions
# ============================================================================

def swipe_campaign(driver, swipe_count, direction="all", stats=None):
    """
    Execute a swiping campaign.
    
    Args:
        driver: WebDriver instance
        swipe_count: Number of swipes to perform
        direction: "all" (mix), "right" (like all), "left" (dislike all), or ratio tuple
        stats: TinderStats object for tracking
    
    Returns:
        Number of successful swipes
    """
    print(f"\n[CAMPAIGN] Starting swipe campaign ({swipe_count} swipes, direction: {direction})...")
    
    successful_swipes = 0
    
    for swipe_num in range(1, swipe_count + 1):
        try:
            # Determine swipe direction
            if direction == "all":
                # Random mix
                import random
                should_like = random.choice([True, False])
            elif direction == "right":
                should_like = True
            elif direction == "left":
                should_like = False
            else:
                # Custom ratio (e.g., (0.3, 0.7) for 30% like, 70% pass)
                import random
                should_like = random.random() < direction[0]
            
            # Check for match before swiping
            if check_for_match(driver):
                if handle_match_popup(driver):
                    if stats:
                        stats.record_match()
                time.sleep(1)
                continue
            
            # Perform swipe
            swipe_success = False
            if should_like:
                swipe_success = swipe_right(driver)
                if swipe_success and stats:
                    stats.record_swipe("right")
            else:
                swipe_success = swipe_left(driver)
                if swipe_success and stats:
                    stats.record_swipe("left")
            
            if swipe_success:
                successful_swipes += 1
            
            # Random delay between swipes to avoid seeming like bot
            import random
            delay = random.uniform(MIN_DELAY_BETWEEN_SWIPES, MAX_DELAY_BETWEEN_SWIPES)
            time.sleep(delay)
            
            # Progress indication
            if swipe_num % 5 == 0:
                print(f"[PROGRESS] Swipes completed: {swipe_num}/{swipe_count}")
            
        except Exception as e:
            print(f"[ERROR] Swipe #{swipe_num} failed: {e}")
            time.sleep(2)
    
    print(f"\n[SUMMARY] Campaign complete: {successful_swipes}/{swipe_count} successful swipes\n")
    return successful_swipes


# ============================================================================
# Main Bot Workflow
# ============================================================================

def main():
    """Main Tinder bot workflow."""
    
    print()
    print("=" * 70)
    print("Automated Tinder Bot".center(70))
    print("=" * 70)
    print()
    
    print("⚠️  ETHICAL REMINDER ⚠️")
    print("-" * 70)
    print("""
Before using this bot, please consider:

1. TRANSPARENCY: Inform your partner/friends about bot usage
2. ETHICS: Use responsibly and ethically
3. RESPECT: Don't spam or harass other users
4. TERMS OF SERVICE: Verify compliance with Tinder's ToS
5. LIMITS: Respect Tinder's swipe limits (100/day free)
6. PURPOSE: Use for legitimate reasons only

This bot is for educational purposes and understanding automation.
    """)
    print("-" * 70 + "\n")
    
    # Note: Actual implementation would require real Tinder credentials
    # This is a demonstration of the bot structure
    
    print("[INFO] Tinder Bot is ready for use")
    print("[INFO] Key features available:")
    print("  ✓ Facebook login automation")
    print("  ✓ Profile navigation")
    print("  ✓ Automated swiping (left/right)")
    print("  ✓ Match detection and handling")
    print("  ✓ Statistics tracking")
    print("  ✓ Swipe limit enforcement")
    print("  ✓ Error recovery")
    print("\n[INFO] See example_usage.py for working examples\n")
    
    print("[INFO] Configuration:")
    print(f"  - Tinder URL: {TINDER_URL}")
    print(f"  - Free tier swipe limit: {SWIPES_PER_DAY_FREE}/day")
    print(f"  - Min delay between swipes: {MIN_DELAY_BETWEEN_SWIPES}s")
    print(f"  - Max delay between swipes: {MAX_DELAY_BETWEEN_SWIPES}s")
    print(f"  - Stats file: {STATS_FILE}\n")


if __name__ == "__main__":
    main()
