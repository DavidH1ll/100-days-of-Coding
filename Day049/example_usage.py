"""
Day 49 - Gym Class Booking Examples
Working code examples showing how to use the gym booking bot

These examples are ready to run and demonstrate common scenarios.
Each example is self-contained and can be copy-pasted into your own code.
"""

from gym_booking_bot import (
    setup_chrome_driver,
    login_to_gym,
    logout_from_gym,
    book_class,
    join_waitlist,
    cancel_booking,
    book_multiple_classes,
    verify_booking,
    access_admin_panel,
    reset_bookings,
    reset_all_data,
    find_class_by_name,
    get_class_status,
    retry_on_failure,
    GYM_PROFILE_NAME,
    TEST_EMAIL,
    TEST_PASSWORD,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import time


# ============================================================================
# EXAMPLE 1: Simple Single Class Booking
# ============================================================================

def example_1_simple_booking():
    """
    Example 1: Book a single class with basic error handling.
    
    Scenario: You want to book your favorite Spin class
    Steps:
    1. Setup browser with persistent profile
    2. Log in with test credentials
    3. Book Spin class
    4. Verify booking in UI
    5. Close browser
    
    Time: ~30 seconds
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Single Class Booking".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Step 1: Setup
        print("[STEP 1] Setting up browser with persistent profile...")
        driver = setup_chrome_driver(profile_name=GYM_PROFILE_NAME)
        
        # Step 2: Log in
        print("\n[STEP 2] Logging in...")
        login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
        
        # Step 3: Book class
        print("\n[STEP 3] Booking Spin class...")
        try:
            book_class(driver, "Spin")
            print("[OK] Booking attempt complete")
        except Exception as e:
            print(f"[ERROR] Booking failed: {e}")
            return False
        
        # Step 4: Verify
        print("\n[STEP 4] Verifying booking...")
        if verify_booking(driver, "Spin"):
            print("[SUCCESS] Booking confirmed in UI!")
            return True
        else:
            print("[ERROR] Booking could not be verified")
            return False
        
    except Exception as e:
        print(f"\n[ERROR] Example failed: {e}")
        return False
        
    finally:
        # Cleanup
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!\n")


# ============================================================================
# EXAMPLE 2: Batch Booking Multiple Classes
# ============================================================================

def example_2_batch_booking():
    """
    Example 2: Book multiple classes in one script run.
    
    Scenario: You want to book your entire weekly schedule
    Classes: Spin (Monday), Yoga (Wednesday), Pilates (Friday)
    
    Steps:
    1. Setup and login
    2. Book multiple classes
    3. Report results
    
    Time: ~1-2 minutes (depends on success/retries)
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Batch Booking Multiple Classes".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        print("[SETUP] Initializing browser and logging in...")
        driver = setup_chrome_driver(profile_name=GYM_PROFILE_NAME)
        login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
        
        # Define classes to book
        classes_to_book = ["Spin", "Yoga", "Pilates"]
        print(f"\n[PLAN] Attempting to book {len(classes_to_book)} classes:")
        for cls in classes_to_book:
            print(f"  → {cls}")
        
        # Book all classes
        print("\n[BOOKING] Starting batch booking...")
        results = book_multiple_classes(driver, classes_to_book)
        
        # Report results
        print("\n" + "-"*70)
        print("BATCH BOOKING RESULTS".center(70))
        print("-"*70)
        
        print(f"\nSuccessful: {len(results['successful'])}/{len(classes_to_book)}")
        if results['successful']:
            for cls in results['successful']:
                print(f"  ✓ {cls}")
        
        print(f"\nFailed: {len(results['failed'])}/{len(classes_to_book)}")
        if results['failed']:
            for cls in results['failed']:
                print(f"  ✗ {cls}")
        
        # Verify each success
        print("\n[VERIFY] Verifying bookings...")
        for cls in results['successful']:
            if verify_booking(driver, cls):
                print(f"  ✓ {cls} confirmed")
            else:
                print(f"  ✗ {cls} NOT confirmed")
        
        return len(results['successful']) > 0
        
    except Exception as e:
        print(f"\n[ERROR] Example failed: {e}")
        return False
        
    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!\n")


# ============================================================================
# EXAMPLE 3: Retry Logic with Network Simulation
# ============================================================================

def example_3_retry_logic():
    """
    Example 3: Demonstrate retry logic handling failures.
    
    Scenario: Network glitches cause booking to fail initially
    The @retry_on_failure decorator handles retries automatically
    
    Steps:
    1. Show decorator in action
    2. Explain exponential backoff
    3. Verify eventual success
    
    Time: ~1-3 minutes (depends on retries)
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Retry Logic with Network Simulation".center(70))
    print("="*70 + "\n")
    
    print("[INFO] Demonstrating @retry_on_failure decorator\n")
    
    print("What happens with retry logic:")
    print("-" * 70)
    print("""
    Attempt 1: Network error → Wait 1 second
    Attempt 2: Timeout → Wait 2 seconds
    Attempt 3: Success! → No more retries
    
    WITHOUT retry logic:
    Attempt 1: Network error → CRASH
    
    WITH @retry_on_failure(max_retries=3, delay=1, backoff=True):
    Attempt 1: Network error → Retry (wait 1s)
    Attempt 2: Timeout → Retry (wait 2s) 
    Attempt 3: Success → Return result
    
    Exponential backoff delays: 1s, 2s, 4s, 8s...
    This prevents overwhelming the server
    """)
    
    print("-" * 70 + "\n")
    
    # Show the decorator in use
    print("[CODE] This is how retry logic works:\n")
    
    print("""
    @retry_on_failure(max_retries=3, delay=1, backoff=True)
    def book_class(driver, class_name):
        # Your booking code here
        button = find_button(driver, "Book Class")
        button.click()
        # If this fails, decorator automatically retries
        # Up to 3 times with increasing delays
    
    # Usage:
    book_class(driver, "Spin")  # Retries handled automatically!
    """)
    
    print("-" * 70 + "\n")
    
    driver = None
    try:
        print("[DEMO] Running with retry logic...\n")
        driver = setup_chrome_driver(profile_name=GYM_PROFILE_NAME)
        login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
        
        print("[INFO] Attempting booking with @retry_on_failure decorator...")
        print("[INFO] Max retries: 3, Initial delay: 1s, Backoff: exponential\n")
        
        try:
            book_class(driver, "Yoga")
            print("\n[SUCCESS] Booking completed!")
            print("[INFO] Retry logic handled any network issues")
            return True
        except Exception as e:
            print(f"\n[ERROR] All retries exhausted: {e}")
            return False
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")
        return False
        
    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!\n")


# ============================================================================
# EXAMPLE 4: Handle Full Classes with Waitlist
# ============================================================================

def example_4_waitlist_handling():
    """
    Example 4: Book class or join waitlist if full.
    
    Scenario: Your favorite class might be full
    Solution: Try booking, if full join waitlist instead
    
    Steps:
    1. Try to book
    2. If full, join waitlist
    3. Report what happened
    
    Time: ~1-2 minutes
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Handle Full Classes with Waitlist".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        print("[SETUP] Initializing browser and logging in...")
        driver = setup_chrome_driver(profile_name=GYM_PROFILE_NAME)
        login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
        
        class_name = "Spin"
        print(f"\n[ATTEMPT] Trying to book: {class_name}\n")
        
        # Check class status first
        class_row = find_class_by_name(driver, class_name)
        if class_row:
            status = get_class_status(driver, class_row)
            print(f"[STATUS] Class status: {status}")
            
            # Try to book
            print(f"\n[BOOKING] Attempting to book {class_name}...")
            try:
                book_class(driver, class_name)
                print(f"[SUCCESS] Booked: {class_name}")
                return True
                
            except Exception as e:
                print(f"[ERROR] Booking failed: {e}")
                
                # If full, try waitlist
                if "full" in str(e).lower():
                    print(f"\n[WAITLIST] Class is full, joining waitlist...")
                    if join_waitlist(driver, class_name):
                        print(f"[SUCCESS] Added to waitlist: {class_name}")
                        return True
                    else:
                        print(f"[ERROR] Couldn't join waitlist")
                        return False
                
                else:
                    print(f"[ERROR] Not a 'full' error, aborting")
                    return False
        else:
            print(f"[ERROR] Class not found: {class_name}")
            return False
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")
        return False
        
    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!\n")


# ============================================================================
# EXAMPLE 5: Test Setup with Admin Panel
# ============================================================================

def example_5_admin_panel_reset():
    """
    Example 5: Use admin panel to reset database before testing.
    
    Scenario: You want to run your bot multiple times
    Problem: After first run, state has changed
    Solution: Reset database before each run
    
    Steps:
    1. Log in as admin
    2. Clear bookings (or reset all)
    3. Log back in as test user
    4. Now database is in known state
    
    Time: ~2-3 minutes
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Test Setup with Admin Panel Reset".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        print("[SETUP] Starting browser session...")
        driver = setup_chrome_driver(profile_name="AdminBot")
        
        # Access admin panel
        print("\n[STEP 1] Accessing admin panel...")
        if not access_admin_panel(driver, ADMIN_EMAIL, ADMIN_PASSWORD):
            print("[ERROR] Failed to access admin panel")
            return False
        
        # Option 1: Reset bookings only
        print("\n[STEP 2] Resetting bookings (keeping users)...")
        if reset_bookings(driver):
            print("[OK] Bookings cleared")
        else:
            print("[ERROR] Failed to reset bookings")
            return False
        
        # Or option 2: Reset everything
        # print("\n[STEP 2] Resetting all data...")
        # if reset_all_data(driver):
        #     print("[OK] All data reset to initial state")
        # else:
        #     print("[ERROR] Failed to reset")
        #     return False
        
        # Log out of admin
        print("\n[STEP 3] Logging out of admin account...")
        logout_from_gym(driver)
        
        # Log back in as test user
        print("\n[STEP 4] Logging in as test user...")
        login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
        
        print("\n[SUCCESS] Database reset complete!")
        print("[INFO] Now ready to run bot with known starting state")
        
        # Optionally book a class to verify
        print("\n[VERIFY] Testing with a booking...")
        if book_class(driver, "Spin"):
            print("[OK] Test booking succeeded")
            return True
        else:
            print("[ERROR] Test booking failed")
            return False
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")
        return False
        
    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!\n")


# ============================================================================
# EXAMPLE 6: Multiple Bot Profiles
# ============================================================================

def example_6_multiple_profiles():
    """
    Example 6: Run multiple bots with different profiles.
    
    Scenario: You have multiple accounts or multiple users
    Solution: Create separate Chrome profiles for each
    
    Steps:
    1. Create driver1 with Profile1
    2. Create driver2 with Profile2
    3. Book different classes with each
    4. Each has independent bookings
    
    Time: ~2-3 minutes
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Multiple Bot Profiles".center(70))
    print("="*70 + "\n")
    
    driver1 = None
    driver2 = None
    try:
        print("[INFO] Setting up two independent bot profiles...\n")
        
        # User 1
        print("[USER 1] Creating first bot profile...")
        driver1 = setup_chrome_driver(profile_name="GymBot_User1")
        login_to_gym(driver1, TEST_EMAIL, TEST_PASSWORD)
        print("[OK] User 1 logged in")
        
        # User 2 (would be different credentials in real scenario)
        print("\n[USER 2] Creating second bot profile...")
        driver2 = setup_chrome_driver(profile_name="GymBot_User2")
        login_to_gym(driver2, TEST_EMAIL, TEST_PASSWORD)  # Same for demo
        print("[OK] User 2 logged in")
        
        # Book different classes
        print("\n[BOOKING] Booking classes with different profiles...")
        
        print("\n  User 1 booking...")
        class1 = "Spin"
        if book_class(driver1, class1):
            print(f"    ✓ {class1} booked by User 1")
        
        print("\n  User 2 booking...")
        class2 = "Yoga"
        if book_class(driver2, class2):
            print(f"    ✓ {class2} booked by User 2")
        
        # Verify independent profiles
        print("\n[VERIFY] Each profile has independent data...")
        
        # Check User 1's bookings
        print("\n  Verifying User 1's bookings...")
        if verify_booking(driver1, class1):
            print(f"    ✓ User 1 has: {class1}")
        
        # Check User 2's bookings
        print("\n  Verifying User 2's bookings...")
        if verify_booking(driver2, class2):
            print(f"    ✓ User 2 has: {class2}")
        
        print("\n[SUCCESS] Multiple profiles working independently!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")
        return False
        
    finally:
        # Cleanup both
        if driver1:
            print("\n[CLEANUP] Closing User 1 browser...")
            driver1.quit()
        if driver2:
            print("[CLEANUP] Closing User 2 browser...")
            driver2.quit()
        print("[OK] Done!\n")


# ============================================================================
# Main Menu
# ============================================================================

def main():
    """Display examples menu."""
    
    print()
    print("="*70)
    print("Day 49 - Gym Class Booking Examples".center(70))
    print("="*70)
    print("""
Choose an example to run:

1. Simple Single Class Booking
   └─ Basic workflow: login → book → verify
   
2. Batch Booking Multiple Classes
   └─ Book your entire weekly schedule
   
3. Retry Logic with Network Simulation
   └─ Demonstrate @retry_on_failure decorator
   
4. Handle Full Classes with Waitlist
   └─ Book or join waitlist if full
   
5. Test Setup with Admin Panel Reset
   └─ Reset database between test runs
   
6. Multiple Bot Profiles
   └─ Run different bots with separate accounts
   
0. Show This Menu

Each example is self-contained and can be copy-pasted.
    """)
    
    print("RECOMMENDATIONS")
    print("-" * 70)
    print("""
Getting Started:
1. Run Example 1 first (simple booking)
2. Review the code to understand flow
3. Try Example 2 (batch booking)
4. Experiment with Example 5 (admin reset)

Advanced:
5. Study retry logic in Example 3
6. Explore multiple profiles in Example 6
7. Try waitlist handling in Example 4

Learning Path:
Example 1 → Example 2 → Example 5 → Example 3 → Example 4 → Example 6
    """)
    
    print("RUNNING EXAMPLES")
    print("-" * 70)
    print("""
To run an example, uncomment the function call at the bottom of this file:

Option A (Direct):
    python example_usage.py
    # Will run examples selected in main()

Option B (Interactive):
    from example_usage import example_1_simple_booking
    example_1_simple_booking()

Option C (All Examples):
    Uncomment all example calls at bottom
    Then: python example_usage.py
    """)
    
    print("="*70)
    print("Examples ready to run!".center(70))
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
    
    # Uncomment any examples to run them:
    # example_1_simple_booking()
    # example_2_batch_booking()
    # example_3_retry_logic()
    # example_4_waitlist_handling()
    # example_5_admin_panel_reset()
    # example_6_multiple_profiles()
    
    print("\nTo run an example, uncomment the function call above.")
    print("Then run: python example_usage.py\n")
