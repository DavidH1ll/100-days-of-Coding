# Day 49 - Gym Class Booking Automation with Selenium

Master advanced Selenium automation by building a real-world gym class booking bot that handles persistent browser profiles, retry logic, dynamic content, and network failures.

## Project: Snack and Lift - Dream Gym Booking System

### The Real-World Problem

You want to book your favorite spin class, but bookings open at midnight. By the time you remember to book it, the class is full. You check again tomorrow, and it's been cancelled. Sound familiar?

This project solves that problem by automating the booking process using Selenium. Your bot wakes up at midnight, logs in, and books your favorite classes while you sleep.

### Project Goals

- Build a Selenium bot that automatically books gym classes
- Use persistent browser profiles to maintain login across sessions
- Implement retry logic to handle network failures gracefully
- Verify bookings actually succeeded before reporting success
- Manage multiple bookings efficiently
- Reset database state for reliable testing

## Key Concepts

### 1. Persistent Browser Profiles

**Problem:** Each time the bot runs, the browser forgets the login.

**Solution:** Use Chrome user profiles to persist login data.

```python
# Create dedicated profile for the bot
driver = setup_chrome_driver(profile_name="GymBot")

# Profile location: C:\Users\[User]\AppData\Local\Google\Chrome\User Data\Default
# Login credentials are remembered across bot runs
```

**Why It Matters:**
- Bot appears as same user to the website
- Session cookies are maintained
- Login is required only once
- More realistic bot behavior

**How It Works:**
1. Chrome profiles stored in Windows user data directory
2. Each profile has separate database (IndexedDB)
3. When bot launches with same profile, browser loads saved state
4. Login cookies and session data are present

### 2. Decorator Pattern for Retry Logic

**Problem:** Network errors crash the bot without retrying.

**Solution:** Use decorators to wrap functions with retry logic.

```python
@retry_on_failure(max_retries=3, delay=1, backoff=True)
def book_class(driver, class_name):
    # Function automatically retried up to 3 times
    # Delays: 1s, 2s, 4s (exponential backoff)
    # Returns on first success or raises after 3 failures

book_class(driver, "Spin")  # Handles retries automatically
```

**Key Features:**
- Automatic retry on exception
- Exponential backoff (delays increase: 1s → 2s → 4s)
- Clear logging of retry attempts
- Preserves function metadata with `@wraps`

**When to Use:**
- Network operations that might be flaky
- Browser interactions that timeout occasionally
- API calls that fail intermittently
- Any operation with external dependencies

### 3. Higher-Order Functions for Flexible Retries

**Problem:** Different scenarios need different retry conditions.

**Solution:** Use higher-order functions to create custom retry decorators.

```python
def is_booking_confirmed(driver):
    return "booked" in driver.page_source.lower()

@retry_with_condition(is_booking_confirmed, max_retries=5)
def book_and_verify(driver, class_name):
    # Retry until condition is met or max attempts reached
    # Condition checked: is booking confirmed?

book_and_verify(driver, "Yoga")  # Retries until confirmed
```

**Advantages:**
- Specialized retry strategies per scenario
- Business logic in condition functions
- Reusable across different operations
- Clear intent in code

### 4. State Verification

**Problem:** We can't be sure if a booking actually succeeded.

**Solution:** Verify booking in UI after booking attempt.

```python
def verify_booking(driver, class_name):
    # Check if class shows as booked
    class_row = find_class_by_name(driver, class_name)
    text = class_row.text.lower()
    
    # Look for confirmation indicators
    return "booked" in text or "cancel" in text

# Use after booking
if book_class(driver, "Spin"):
    if verify_booking(driver, "Spin"):
        print("✓ Booking confirmed!")
    else:
        print("✗ Booking failed or not visible")
```

**What We Check:**
- "Booked" or "Confirmed" text in UI
- "Cancel" button (only visible for booked classes)
- Element attributes (data-booked, etc.)
- Success message appears

### 5. Admin Panel Operations

**Problem:** Need to reset database state between test runs.

**Solution:** Use admin functions to manage database.

```python
# Access admin panel
access_admin_panel(driver, "admin@test.com", "admin123")

# Clear only the bookings (keep user accounts)
reset_bookings(driver)

# OR reset everything to initial state
reset_all_data(driver)
```

**Admin Capabilities:**
- View current database state
- Clear bookings only (users remain)
- Reset all data (full reset)
- View database stats

**Testing Workflow:**
```
1. Reset database (admin panel)
2. Run booking bot
3. Verify bookings in UI
4. Reset database
5. Run bot again (clean slate)
```

### 6. Batch Operations

**Problem:** Booking multiple classes requires repetitive code.

**Solution:** Batch operation function.

```python
classes = ["Spin", "Yoga", "Pilates"]
results = book_multiple_classes(driver, classes)

print(results)
# {
#   'successful': ['Spin', 'Pilates'],
#   'failed': ['Yoga']  # maybe full or error
# }
```

**Advantages:**
- Single function call for multiple bookings
- Automatic error handling per class
- Summary of results
- Easy to extend

## Code Structure

### Core Functions

#### Browser Setup
- `setup_chrome_driver()` - Initialize WebDriver with profile
- `create_chrome_profile()` - Create/locate Chrome profile

#### Authentication
- `login_to_gym()` - Log in with email/password
- `logout_from_gym()` - Log out and clean up

#### Booking Operations
- `find_class_by_name()` - Locate class in bookings page
- `get_class_status()` - Check if available/full/etc
- `book_class()` - Book a class (with retry logic)
- `join_waitlist()` - Join waitlist for full class
- `cancel_booking()` - Cancel existing booking
- `verify_booking()` - Confirm booking succeeded

#### Batch Operations
- `book_multiple_classes()` - Book list of classes
- `handle_network_simulation()` - Test network failures

#### Admin Functions
- `access_admin_panel()` - Log in as admin
- `reset_bookings()` - Clear bookings only
- `reset_all_data()` - Full database reset

### Decorators

#### @retry_on_failure
Retry function on any exception with exponential backoff.

```python
@retry_on_failure(max_retries=3, delay=1, backoff=True)
def critical_function(driver):
    # Retried on any exception
    pass
```

#### @retry_with_condition
Retry until condition function returns True.

```python
@retry_with_condition(condition_func, max_retries=5)
def function_to_retry(driver):
    # Retried until condition is met
    pass
```

## The Snack and Lift Website

### Credentials
- **Student Account:**
  - Email: `student@Test.com`
  - Password: `password123`
- **Admin Account:**
  - Email: `admin@test.com`
  - Password: `admin123`

### Pages
- **Landing Page:** Testimonials and project info
- **Login Page:** Email/password authentication
- **Bookings Page:** Available classes and booking status
- **Admin Panel:** Database management and stats

### Class States
- **Available:** "Book Class" button enabled
- **Full:** "Join Waitlist" button enabled
- **Booked:** "Cancel" button (you have it booked)
- **On Waitlist:** "Leave Waitlist" button

### Browser Database
- **Storage Type:** IndexedDB (browser local storage)
- **Location:** Chrome DevTools → Application → Storage → IndexedDB
- **Scope:** Per profile/browser instance
- **Persistence:** Survives browser restart

## Best Practices

### 1. Always Use Persistent Profiles

```python
# Good - profile data persists
driver = setup_chrome_driver(profile_name="GymBot")

# Bad - profile data lost after each run
driver = webdriver.Chrome()  # Uses temporary profile
```

### 2. Implement Retry Logic for Network Operations

```python
# Good - handles network failures
@retry_on_failure(max_retries=3, delay=1)
def book_class(driver, class_name):
    # Try up to 3 times

# Bad - crashes on network error
def book_class_bad(driver, class_name):
    # One attempt, fails hard on error
```

### 3. Verify Success, Don't Assume It

```python
# Good - verify and confirm
book_class(driver, "Spin")
if verify_booking(driver, "Spin"):
    print("✓ Confirmed booked")

# Bad - assume success
book_class(driver, "Spin")
print("✓ Booked (maybe)")  # We don't actually know
```

### 4. Use Admin Panel for Testing

```python
# Good - reset before each test run
access_admin_panel(driver, admin_email, admin_password)
reset_bookings(driver)
# Now run bot with clean state

# Bad - don't reset, state changes
# Bot might behave differently on second run
```

### 5. Handle Full Classes Gracefully

```python
# Good - try booking, fallback to waitlist
try:
    book_class(driver, "Spin")
except:
    print("Full, trying waitlist...")
    join_waitlist(driver, "Spin")

# Bad - crash if class is full
book_class(driver, "Spin")  # Fails if full
```

### 6. Separate Concerns

```python
# Good - focused functions
login_to_gym(driver, email, password)  # Auth
book_class(driver, class_name)         # Booking
verify_booking(driver, class_name)     # Verification

# Bad - mixed concerns
def do_everything(driver, email, password, class_name):
    # Login + booking + verification (hard to test)
```

## Real-World Patterns Demonstrated

### Decorator Pattern
```python
@retry_on_failure(max_retries=3)
def operation():
    # Function wrapped with retry logic
    pass
```

**When to Use:**
- Retry logic
- Logging and timing
- Access control
- Caching

### Higher-Order Functions
```python
def create_retry_decorator(condition):
    def decorator(func):
        # Custom retry logic based on condition
        pass
    return decorator

@create_retry_decorator(my_condition)
def operation():
    pass
```

**When to Use:**
- Flexible customization
- Conditional behavior
- Factory patterns
- Dependency injection

### Context Managers (Could Use)
```python
class BrowserSession:
    def __enter__(self):
        self.driver = setup_chrome_driver()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

with BrowserSession() as driver:
    login_to_gym(driver, email, password)
    # Browser auto-closed after block
```

**When to Use:**
- Resource management
- Setup/cleanup
- Guaranteed cleanup even on error

## Common Challenges & Solutions

### Challenge 1: Browser loses login between runs

**Problem:**
```python
# Run 1
driver = webdriver.Chrome()
login_to_gym(driver, "student@test.com", "password123")
driver.quit()

# Run 2
driver = webdriver.Chrome()  # NOT logged in!
```

**Solution:**
```python
# Run 1
driver = setup_chrome_driver(profile_name="GymBot")
login_to_gym(driver, "student@test.com", "password123")
driver.quit()

# Run 2
driver = setup_chrome_driver(profile_name="GymBot")
# Still logged in! Profile persists data
```

**Why It Works:**
Chrome profiles store cookies, cache, and local storage that survive browser restarts.

### Challenge 2: Network error crashes bot

**Problem:**
```python
@retry_on_failure(max_retries=0)  # No retries
def book_class(driver, class_name):
    button.click()  # Network error crashes here

book_class(driver, "Spin")  # Bot crashes
```

**Solution:**
```python
@retry_on_failure(max_retries=3, delay=1, backoff=True)
def book_class(driver, class_name):
    button.click()  # First attempt fails
                    # Auto-retry 1 (after 1s)
                    # Auto-retry 2 (after 2s)
                    # Auto-retry 3 (after 4s)
                    # Success on retry 2

book_class(driver, "Spin")  # Bot continues despite glitches
```

### Challenge 3: Can't verify if booking succeeded

**Problem:**
```python
def book_class(driver, class_name):
    button.click()
    return True  # We assume it worked, but we don't know!

book_class(driver, "Spin")  # Returns True, but might have failed
```

**Solution:**
```python
def book_class(driver, class_name):
    button.click()
    time.sleep(1)
    return verify_booking(driver, class_name)  # Actually check!

if book_class(driver, "Spin"):  # Know for sure it worked
    print("✓ Confirmed in UI")
```

### Challenge 4: Database state keeps changing

**Problem:**
```python
# Run 1 - books one class
book_class(driver, "Spin")  # Success

# Run 2 - different classes available now
book_class(driver, "Spin")  # Might be different state now
```

**Solution:**
```python
# Run 1
access_admin_panel(driver, admin_email, admin_password)
reset_bookings(driver)  # Clean slate
book_class(driver, "Spin")
driver.quit()

# Run 2
driver = setup_chrome_driver(profile_name="AdminBot")
access_admin_panel(driver, admin_email, admin_password)
reset_bookings(driver)  # Same state as before
book_class(driver, "Spin")  # Consistent behavior
```

### Challenge 5: Multiple bots interfere with each other

**Problem:**
```python
driver1 = webdriver.Chrome()  # Default profile
driver2 = webdriver.Chrome()  # Same profile!

login_to_gym(driver1, "user1@test.com", ...)
login_to_gym(driver2, "user2@test.com", ...)
# Both logged in as user2 (conflict!)
```

**Solution:**
```python
driver1 = setup_chrome_driver(profile_name="User1Bot")
driver2 = setup_chrome_driver(profile_name="User2Bot")

login_to_gym(driver1, "user1@test.com", ...)
login_to_gym(driver2, "user2@test.com", ...)
# Each has own profile, independent bookings
```

## Advanced Features

### Time Simulation
Test bot behavior across different days/times.

```python
# Bookings available on different days
# Bot should work regardless of current time
# Use browser time simulation (DevTools) for testing
```

### Network Simulation
Test bot recovery from network failures.

```python
# Enable network throttling in Chrome DevTools
# Bot should retry and eventually succeed
# Verify @retry_on_failure works under load
```

### Multiple Account Management
Run different bots for different users.

```python
user1_driver = setup_chrome_driver(profile_name="GymBot_User1")
user2_driver = setup_chrome_driver(profile_name="GymBot_User2")

login_to_gym(user1_driver, "user1@test.com", "password123")
login_to_gym(user2_driver, "user2@test.com", "password123")

# Each user books independently
book_multiple_classes(user1_driver, classes_for_user1)
book_multiple_classes(user2_driver, classes_for_user2)
```

## Testing Workflow

### Test Setup
```python
# 1. Access admin panel
access_admin_panel(driver, ADMIN_EMAIL, ADMIN_PASSWORD)

# 2. Reset to known state
reset_bookings(driver)

# 3. Log out and return to normal user
logout_from_gym(driver)
login_to_gym(driver, TEST_EMAIL, TEST_PASSWORD)
```

### Run Bot
```python
# 4. Execute booking logic
classes = ["Spin", "Yoga", "Pilates"]
results = book_multiple_classes(driver, classes)

# 5. Verify results
assert len(results['successful']) > 0
assert all(verify_booking(driver, cls) for cls in results['successful'])
```

### Verify in UI
```python
# 6. Manually check bookings page
# Should see booked classes with "Cancel" button
# Matches bot's reported success list
```

### Clean Up
```python
# 7. Reset for next test
access_admin_panel(driver, ADMIN_EMAIL, ADMIN_PASSWORD)
reset_bookings(driver)
driver.quit()
```

## Project Extensions

### Basic
- [x] Book single class
- [x] Book multiple classes
- [x] Handle full classes with waitlist
- [x] Verify bookings

### Intermediate
- [ ] Schedule bot to run at specific time
- [ ] Email notifications on success
- [ ] Track booking history
- [ ] Support multiple users

### Advanced
- [ ] SMS/Slack notifications
- [ ] Booking dashboard
- [ ] Class recommendations
- [ ] Preference learning
- [ ] CAPTCHA handling

### Production
- [ ] Robust logging
- [ ] Error monitoring
- [ ] Database persistence
- [ ] Proxy support
- [ ] Headless operation

## Key Takeaways

✅ **Persistent Profiles:** Browser profiles maintain login across sessions  
✅ **Decorator Pattern:** @retry_on_failure wraps functions with retry logic  
✅ **Higher-Order Functions:** Flexible, reusable retry strategies  
✅ **State Verification:** Confirm success before declaring victory  
✅ **Batch Operations:** Efficiently handle multiple bookings  
✅ **Admin Panel:** Reset database for reliable testing  
✅ **Error Handling:** Gracefully recover from network failures  

## Skills Demonstrated

- ✓ Advanced Selenium patterns
- ✓ Python decorators and higher-order functions
- ✓ Browser profile management
- ✓ Retry logic and error recovery
- ✓ State management and verification
- ✓ Professional automation architecture
- ✓ Testing and quality assurance
- ✓ Real-world problem solving

## Summary

Day 49 teaches professional-grade automation skills by solving a real-world problem: automated gym class bookings. You learn not just Selenium, but software engineering patterns like decorators, higher-order functions, and robust error handling. These skills apply to any booking system—restaurants, tickets, courses, meetings.

The bot demonstrates that automation isn't just about clicking buttons. It's about building reliable, recoverable systems that handle failures gracefully and verify their own success.

Good luck with your Day 49 project! Never miss another class booking! 🎯💪

---

**Next Steps:**
1. Review `gym_booking_bot.py` to understand implementation
2. Check `example_usage.py` for copy-paste ready examples
3. Run your first booking script
4. Experiment with retry logic and admin panel
5. Extend with notifications or scheduling

**Questions?** Review the README and example_usage.py, then experiment!
