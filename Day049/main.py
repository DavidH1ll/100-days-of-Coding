"""
Day 49 - Gym Class Booking Automation with Selenium

Automate gym class bookings using Selenium, persistent browser profiles,
retry logic, and advanced automation techniques.

Project: Snack and Lift - Dream Gym Booking System
Challenge: Never miss a class booking again!

Real Scenario:
The booking system opens at midnight, but you're already in pajamas. 
This bot books your favorite classes automatically while you sleep!

Key Concepts:
1. Persistent browser profiles (remembers user login across sessions)
2. Login automation (simulating real user authentication)
3. Dynamic content handling (date/time sensitive bookings)
4. Retry logic and error recovery (decorators and wrappers)
5. State verification (confirming bookings actually succeeded)
6. Batch operations (booking multiple classes)
7. Network resilience (handling network failures gracefully)
8. Admin panel operations (database management and reset)

Skills Developed:
- Higher-order functions for retry logic
- Decorator pattern for error handling
- Complex state management and verification
- Working with persistent browser data (IndexedDB)
- Handling dynamic content and timing issues
- Professional automation patterns and best practices

Real-World Applications:
- Gym and fitness class bookings
- Meeting room reservations
- Course and seminar registrations
- Ticket bookings (concerts, sports, etc.)
- Table reservations at restaurants
- Medical appointment bookings
- Any time-sensitive booking system

Quick Start:
1. Open gym_booking_bot.py to see the implementation
2. Check example_usage.py for usage patterns
3. Read README.md for detailed documentation

Concepts Covered:
- Browser profile management (persistent storage)
- Decorator pattern for retries (@retry_on_failure)
- Higher-order functions (retry_with_condition)
- Wait strategies and timeouts
- Element state verification
- Error handling and recovery
- Admin panel operations
- Database reset and testing
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
    retry_on_failure,
    GYM_PROFILE_NAME,
    TEST_EMAIL,
    TEST_PASSWORD,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)


def display_project_info():
    """Display project information and key concepts."""
    
    print()
    print("=" * 70)
    print("Day 49 - Snack and Lift Gym Booking Automation Bot".center(70))
    print("=" * 70)
    print()
    
    print("PROJECT OVERVIEW")
    print("-" * 70)
    print("""
Snack and Lift is a dream gym with a motto: "Lift weights, eat snacks, repeat."

The Problem:
- Gym classes book up within minutes of becoming available
- Bookings open at midnight
- You're asleep and miss out on your favorite classes

The Solution:
- Use Selenium to automate class bookings
- Keep bot running at midnight
- Wake up to confirmed bookings!

Key Features:
✓ Persistent browser profiles (remembers login)
✓ Retry logic for network failures
✓ Multiple class booking in batch
✓ Verification that bookings succeeded
✓ Admin panel for database management
✓ Time and network simulation support
    """)
    
    print("KEY CONCEPTS & PATTERNS")
    print("-" * 70)
    print("""
1. PERSISTENT BROWSER PROFILES
   Problem: Bot loses login between runs
   Solution: Use Chrome profiles to maintain session
   Benefit: Bot recognizes same user across sessions
   
   Profile stored at: C:\\Users\\[Username]\\AppData\\Local\\Google\\Chrome\\User Data
   Each bot has dedicated profile folder (e.g., GymBot)

2. DECORATOR PATTERN FOR RETRIES
   Problem: Network failures cause bot to crash
   Solution: @retry_on_failure decorator wraps functions
   Benefit: Automatic retry with exponential backoff
   
   Example:
   @retry_on_failure(max_retries=3, delay=1, backoff=True)
   def book_class(driver, class_name):
       # Function attempts up to 3 times
       # Delay: 1s, 2s, 4s (exponential)

3. HIGHER-ORDER FUNCTIONS
   Problem: Need different retry conditions per scenario
   Solution: Higher-order functions return decorated functions
   Benefit: Flexible, reusable retry strategies
   
   Example:
   @retry_with_condition(is_booking_confirmed, max_retries=5)
   def book_and_verify(driver, class_name):
       # Retry until booking confirmed

4. STATE VERIFICATION
   Problem: Can't be sure if booking succeeded
   Solution: verify_booking() checks UI after booking
   Benefit: Know for certain if class is booked
   
   Checks: "Booked" text, "Cancel" button presence

5. ADMIN PANEL OPERATIONS
   Problem: Need to reset database between test runs
   Solution: Admin functions for database management
   Benefit: Repeatable, controlled test scenarios
   
   Operations: reset_bookings(), reset_all_data()

6. BATCH OPERATIONS
   Problem: Manually booking classes is tedious
   Solution: book_multiple_classes() handles list
   Benefit: Book entire schedule in one call
   
   Returns: {'successful': [...], 'failed': [...]}
    """)
    
    print("THE GYM WEBSITE")
    print("-" * 70)
    print("""
Login Credentials (Test Account):
  Email:    student@Test.com
  Password: password123

Login Credentials (Admin):
  Email:    admin@test.com
  Password: admin123

Website Features:
- Landing page with testimonials
- Login/Register functionality
- Bookings page showing available classes
- Admin panel for database management

Key Buttons & States:
- "Book Class" - Class has availability
- "Join Waitlist" - Class is full
- "Cancel" - You are booked
- "Leave Waitlist" - You're on waitlist

Database (Browser IndexedDB):
- Stored locally in browser
- Different per profile/user
- Viewable in Chrome DevTools → Application → Storage

Time & Network Simulation:
- Time simulation: Test behavior across different days
- Network simulation: Test retry logic under failures
- Disabled by default, enable only for advanced testing
    """)
    
    print("AUTOMATION WORKFLOW")
    print("-" * 70)
    print("""
TYPICAL BOT RUN:

1. Setup Browser
   └─ Load Chrome with persistent profile
   └─ Profile remembers login credentials

2. Login
   └─ Navigate to gym website
   └─ Enter email and password
   └─ Wait for dashboard to load
   └─ @retry_on_failure handles network issues

3. Book Classes
   └─ Find each class in list
   └─ Check class status (Available/Full/etc)
   └─ Click "Book Class" button
   └─ Verify booking in UI
   └─ Handle full classes with waitlist

4. Report Results
   └─ Summary of successful bookings
   └─ List of failed bookings with reasons
   └─ Keep browser open for verification

5. Cleanup
   └─ Logout (optional)
   └─ Close browser

ADVANCED SCENARIOS:

Reset Before Testing:
   1. Access admin panel
   2. Click "Reset Bookings Only" or "Reset All Data"
   3. Run bot script
   4. Verify bookings in UI

Handle Network Failures:
   1. Enable network simulation (DevTools)
   2. Run bot - @retry_on_failure will handle retries
   3. Verify bot recovers from failures

Test Multiple Profiles:
   1. Create separate Chrome profiles
   2. Use different bot instances per profile
   3. Each profile has independent bookings
    """)
    
    print("PROFESSIONAL PATTERNS DEMONSTRATED")
    print("-" * 70)
    print("""
✓ DECORATOR PATTERN
  @retry_on_failure wraps functions for retry logic
  Keeps code DRY and readable

✓ HIGHER-ORDER FUNCTIONS
  Parametric retry strategies for different scenarios
  Flexible and composable

✓ CONTEXT MANAGERS (Optional)
  Could use 'with' for browser management
  Ensures cleanup even on errors

✓ EXCEPTION HANDLING
  Specific exception catching
  Graceful degradation

✓ STATE MANAGEMENT
  Tracking booking state and UI state
  Verification of successful actions

✓ LOGGING & MONITORING
  Detailed console output for debugging
  Clear indication of success/failure

✓ PERSISTENT STORAGE
  Chrome profiles maintain session
  Bot appears as same user each run

✓ CONFIGURATION MANAGEMENT
  Constants for timeouts, URLs, credentials
  Easy to modify for different scenarios
    """)
    
    print("COMMON CHALLENGES & SOLUTIONS")
    print("-" * 70)
    print("""
CHALLENGE 1: "Browser loses login between runs"
SOLUTION: Use persistent Chrome profile
  driver = setup_chrome_driver(profile_name="GymBot")
  Profile stored: ~/.../Chrome/User Data/Default
  Login is remembered across bot runs

CHALLENGE 2: "Network error on button click crashes bot"
SOLUTION: Use @retry_on_failure decorator
  @retry_on_failure(max_retries=3, delay=1, backoff=True)
  def book_class(driver, class_name):
      # Auto-retries on any exception
  # Exponential backoff: 1s → 2s → 4s

CHALLENGE 3: "Can't verify if booking actually succeeded"
SOLUTION: Call verify_booking() after booking
  book_class(driver, "Spin")
  if verify_booking(driver, "Spin"):
      print("✓ Booking confirmed")
  # Checks for "Booked" text and "Cancel" button

CHALLENGE 4: "Need to test same scenario multiple times"
SOLUTION: Use admin reset functions
  access_admin_panel(driver, ADMIN_EMAIL, ADMIN_PASSWORD)
  reset_bookings(driver)  # Clear only bookings, keep users
  # OR
  reset_all_data(driver)  # Full reset to initial state

CHALLENGE 5: "Multiple bot instances interfere with each other"
SOLUTION: Create separate Chrome profiles per bot
  driver1 = setup_chrome_driver(profile_name="GymBot1")
  driver2 = setup_chrome_driver(profile_name="GymBot2")
  # Each profile has independent database

CHALLENGE 6: "Can't reliably wait for dynamic content"
SOLUTION: Use WebDriverWait with explicit conditions
  WebDriverWait(driver, TIMEOUT).until(
      EC.element_to_be_clickable((By.NAME, "password"))
  )
  # Waits up to TIMEOUT for element to be clickable
    """)
    
    print("TESTING CHECKLIST")
    print("-" * 70)
    print("""
Before running bot:
□ Chrome browser installed
□ ChromeDriver in PATH or specified
□ Internet connection working
□ Test account created (student@Test.com, password123)
□ Database reset if needed (admin panel)

After running bot:
□ Check bookings appear in browser UI
□ Verify booking confirmations visible
□ Check "Cancel" button present for booked classes
□ Review console output for errors
□ Check Chrome profile data (DevTools → Application → IndexedDB)

Advanced testing:
□ Test with network simulation enabled
□ Test retry logic by introducing delays
□ Test multiple profile interference
□ Test database reset procedures
□ Test error handling with intentional failures
    """)
    
    print("NEXT STEPS & EXTENSIONS")
    print("-" * 70)
    print("""
Basic Implementation:
→ Book single class with verification
→ Book multiple classes in batch
→ Handle full classes with waitlist
→ Reset database between runs

Intermediate:
→ Schedule bot to run at midnight
→ Email notifications on success/failure
→ Support multiple user accounts
→ Track booking history

Advanced:
→ Notification system (SMS, Slack, Discord)
→ Dashboard for booking status
→ Machine learning to predict availability
→ User preferences and preferences scheduling
→ Class recommendation engine

Production Ready:
→ Robust error handling and logging
→ Monitoring and alerting
→ Database persistence
→ Multiple proxy support
→ CAPTCHA handling
→ Headless operation mode
    """)
    
    print("=" * 70)
    print("Ready to automate gym class bookings!".center(70))
    print("=" * 70)
    print()


def display_usage_examples():
    """Show how to use the gym booking bot."""
    
    print("USAGE EXAMPLES")
    print("-" * 70)
    print("""
1. SIMPLE BOOKING
   from gym_booking_bot import setup_chrome_driver, login_to_gym, book_class
   
   driver = setup_chrome_driver(profile_name="GymBot")
   login_to_gym(driver, "student@Test.com", "password123")
   book_class(driver, "Spin")
   driver.quit()

2. BATCH BOOKING
   from gym_booking_bot import book_multiple_classes
   
   classes = ["Spin", "Yoga", "Pilates"]
   results = book_multiple_classes(driver, classes)
   print(f"Booked: {results['successful']}")
   print(f"Failed: {results['failed']}")

3. RETRY LOGIC
   @retry_on_failure(max_retries=3, delay=1, backoff=True)
   def reliable_booking(driver, class_name):
       return book_class(driver, class_name)

4. ADMIN OPERATIONS
   access_admin_panel(driver, "admin@test.com", "admin123")
   reset_bookings(driver)  # Clear bookings only
   # Now run bot again with clean slate

5. WAITLIST HANDLING
   try:
       book_class(driver, "Full Class")
   except:
       join_waitlist(driver, "Full Class")

6. MULTIPLE PROFILES
   driver1 = setup_chrome_driver(profile_name="User1")
   driver2 = setup_chrome_driver(profile_name="User2")
   # Independent bookings per profile

See example_usage.py for complete working examples.
    """)


def main():
    """Main information display."""
    
    display_project_info()
    display_usage_examples()
    
    print("\nFILES IN THIS PROJECT")
    print("-" * 70)
    print("""
gym_booking_bot.py
  └─ Core bot implementation
  └─ All functions and decorators
  └─ Retry logic, login, booking operations
  └─ Admin panel functions

main.py (this file)
  └─ Project overview
  └─ Key concepts explanation
  └─ Usage examples
  └─ Testing checklist

example_usage.py
  └─ Practical working examples
  └─ Different scenarios and use cases
  └─ Copy-paste ready code

README.md
  └─ Complete documentation
  └─ Detailed concept explanations
  └─ Best practices and patterns
  └─ Troubleshooting guide
    """)
    
    print("\nGETTING STARTED")
    print("-" * 70)
    print("""
Step 1: Review the concepts in this file
Step 2: Look at example_usage.py for working code
Step 3: Study gym_booking_bot.py implementation
Step 4: Run your first booking script
Step 5: Read README.md for deep dives

Questions?
→ Check README.md for detailed explanations
→ Review example_usage.py for working code samples
→ Study the decorators and higher-order functions
→ Experiment with the admin panel operations

Ready? Open example_usage.py to get started!
    """)
    
    print("\n" + "=" * 70)
    print("[SUCCESS] Gym booking bot ready to use!".center(70))
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
