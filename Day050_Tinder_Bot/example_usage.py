"""
Day 50 - Tinder Bot Examples
Working code examples showing how to use the Tinder automation bot

These examples demonstrate different automation scenarios.
Each example is self-contained and can be adapted to your needs.

⚠️  IMPORTANT: Always use ethically and responsibly!
"""

from tinder_bot import (
    setup_tinder_driver,
    login_to_tinder_facebook,
    handle_initial_prompts,
    swipe_right,
    swipe_left,
    swipe_campaign,
    check_for_match,
    handle_match_popup,
    TinderStats,
    SWIPES_PER_DAY_FREE,
    TINDER_URL,
)
import time


# ============================================================================
# EXAMPLE 1: Simple Swiping Campaign
# ============================================================================

def example_1_simple_swiping():
    """
    Example 1: Simple automated swiping campaign.
    
    Scenario: Swipe through profiles with 50/50 like/pass ratio
    
    Steps:
    1. Setup browser
    2. Log in via Facebook
    3. Handle initial prompts
    4. Perform 10 swipes (example, normally 100)
    5. Report statistics
    
    Time: ~2-3 minutes
    
    Security Note:
    For actual use, DON'T hardcode credentials!
    Use environment variables:
    
    import os
    email = os.environ.get('FACEBOOK_EMAIL')
    password = os.environ.get('FACEBOOK_PASSWORD')
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Swiping Campaign".center(70))
    print("="*70 + "\n")
    
    # CREDENTIALS - NEVER hardcode in production!
    # Use environment variables instead
    FACEBOOK_EMAIL = "your_email@example.com"
    FACEBOOK_PASSWORD = "your_password"
    
    driver = None
    stats = TinderStats()
    
    try:
        print("[EXAMPLE 1] Starting simple swiping campaign...\n")
        
        # Setup
        print("[STEP 1] Setting up browser...")
        driver = setup_tinder_driver(headless=False)
        
        # Login
        print("[STEP 2] Logging in...")
        if not login_to_tinder_facebook(driver, FACEBOOK_EMAIL, FACEBOOK_PASSWORD):
            print("[ERROR] Login failed")
            return False
        
        # Handle prompts
        print("[STEP 3] Handling initial prompts...")
        handle_initial_prompts(driver)
        
        # Swipe campaign
        print("[STEP 4] Starting swiping campaign...")
        print("[INFO] Target: 10 swipes (example, normally 100)")
        swipe_campaign(driver, swipe_count=10, direction="all", stats=stats)
        
        # Report
        print("[STEP 5] Reporting statistics...")
        stats.end_session(10)
        stats.print_summary()
        
        print("[SUCCESS] Campaign complete!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}\n")
        return False
        
    finally:
        if driver:
            print("[CLEANUP] Closing browser...")
            driver.quit()


# ============================================================================
# EXAMPLE 2: Batch Swiping with Daily Limit
# ============================================================================

def example_2_batch_with_limit():
    """
    Example 2: Batch swiping respecting daily limits.
    
    Scenario: Swipe exactly 100 times (free tier limit) per session
    
    Features:
    - Enforce Tinder's 100 swipes/day limit
    - Track progress
    - Report time saved
    
    Time: ~2-5 minutes
    
    Why Important:
    - Tinder enforces 100 swipes/day for free users
    - Trying to exceed gets account flagged
    - Responsible bot respects limits
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Batch Swiping with Daily Limit".center(70))
    print("="*70 + "\n")
    
    FACEBOOK_EMAIL = "your_email@example.com"
    FACEBOOK_PASSWORD = "your_password"
    
    driver = None
    stats = TinderStats()
    
    try:
        print("[EXAMPLE 2] Batch swiping with daily limit enforcement...\n")
        
        print("[INFO] Tinder free tier limit: 100 swipes/day")
        print("[GOAL] Respect and enforce this limit\n")
        
        # Setup
        driver = setup_tinder_driver(headless=False)
        
        # Login
        if not login_to_tinder_facebook(driver, FACEBOOK_EMAIL, FACEBOOK_PASSWORD):
            return False
        
        handle_initial_prompts(driver)
        
        # Swipe exactly 100 times (respecting limit)
        print("[CAMPAIGN] Starting 100-swipe campaign...")
        print("[IMPORTANT] Respecting Tinder's daily limit\n")
        
        swipes_completed = swipe_campaign(
            driver,
            swipe_count=SWIPES_PER_DAY_FREE,  # Exactly 100
            direction="all",  # 50/50 like/pass
            stats=stats
        )
        
        # Record session
        stats.end_session(swipes_completed)
        
        # Report
        print("\n[RESULTS] Daily Limit Campaign")
        print("-" * 70)
        print(f"Swipes Completed: {swipes_completed}/{SWIPES_PER_DAY_FREE}")
        print(f"Limit Respected: {'Yes ✓' if swipes_completed <= SWIPES_PER_DAY_FREE else 'No ✗'}")
        stats.print_summary()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}\n")
        return False
        
    finally:
        if driver:
            driver.quit()


# ============================================================================
# EXAMPLE 3: Like-All Strategy
# ============================================================================

def example_3_like_all_strategy():
    """
    Example 3: "Like-all" strategy (swipe right on everyone).
    
    Scenario: Maximize matches by liking all profiles
    
    Use Case:
    - Higher match volume
    - More opportunities to chat
    - Can be selective in conversations
    
    Trade-offs:
    - Less selective
    - More low-quality matches
    - Takes time to sort through
    
    Ethical Note:
    - Make sure real matches know you're serious
    - Be genuine in conversations
    - Don't ghost people
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Like-All Strategy".center(70))
    print("="*70 + "\n")
    
    FACEBOOK_EMAIL = "your_email@example.com"
    FACEBOOK_PASSWORD = "your_password"
    
    driver = None
    stats = TinderStats()
    
    try:
        print("[EXAMPLE 3] Like-all swiping strategy...\n")
        
        print("[STRATEGY] Swipe right on ALL profiles")
        print("[GOAL] Maximize matches and opportunities")
        print("[CAUTION] More matches = more conversations needed\n")
        
        driver = setup_tinder_driver(headless=False)
        
        if not login_to_tinder_facebook(driver, FACEBOOK_EMAIL, FACEBOOK_PASSWORD):
            return False
        
        handle_initial_prompts(driver)
        
        # Swipe right on everyone
        print("[CAMPAIGN] Starting like-all campaign...")
        swipe_campaign(
            driver,
            swipe_count=50,  # Example: 50 swipes
            direction="right",  # 100% right (like)
            stats=stats
        )
        
        stats.end_session(50)
        
        print("\n[STRATEGY RESULTS]")
        print(f"Right Swipes: {stats.stats['right_swipes']}")
        print(f"Left Swipes: {stats.stats['left_swipes']}")
        print(f"Expected Matches: ~{int(stats.stats['right_swipes'] * 0.005)} " +
              "(based on 0.5% average match rate)")
        
        stats.print_summary()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}\n")
        return False
        
    finally:
        if driver:
            driver.quit()


# ============================================================================
# EXAMPLE 4: Selective Swiping Strategy
# ============================================================================

def example_4_selective_strategy():
    """
    Example 4: Selective swiping (mostly pass, selective likes).
    
    Scenario: Be choosy - only like profiles matching preferences
    
    Use Case:
    - More selective approach
    - Higher quality matches (theoretically)
    - Fewer total matches
    - More likely to result in conversations
    
    Trade-off:
    - Fewer matches overall
    - More discerning selection
    - Current bot can't analyze profiles
    
    Future Enhancement:
    - Add ML to analyze profile images
    - Parse bio text for preferences
    - Location-based filtering
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Selective Swiping Strategy".center(70))
    print("="*70 + "\n")
    
    FACEBOOK_EMAIL = "your_email@example.com"
    FACEBOOK_PASSWORD = "your_password"
    
    driver = None
    stats = TinderStats()
    
    try:
        print("[EXAMPLE 4] Selective swiping strategy...\n")
        
        print("[STRATEGY] Swipe right on only ~30% of profiles")
        print("[GOAL] Higher quality matches, fewer time wasters")
        print("[NOTE] Current bot can't analyze profiles - upgrade with ML!\n")
        
        driver = setup_tinder_driver(headless=False)
        
        if not login_to_tinder_facebook(driver, FACEBOOK_EMAIL, FACEBOOK_PASSWORD):
            return False
        
        handle_initial_prompts(driver)
        
        # Swipe with 30% like, 70% pass ratio
        print("[CAMPAIGN] Starting selective campaign...")
        print("[RATIO] 30% like, 70% pass\n")
        swipe_campaign(
            driver,
            swipe_count=50,
            direction=(0.3, 0.7),  # 30% like, 70% pass
            stats=stats
        )
        
        stats.end_session(50)
        
        print("\n[STRATEGY RESULTS]")
        print(f"Total Swipes: {stats.stats['total_swipes']}")
        print(f"Right Swipes: {stats.stats['right_swipes']} " +
              f"({stats.stats['right_swipes']/stats.stats['total_swipes']*100:.1f}%)")
        print(f"Left Swipes: {stats.stats['left_swipes']} " +
              f"({stats.stats['left_swipes']/stats.stats['total_swipes']*100:.1f}%)")
        
        stats.print_summary()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}\n")
        return False
        
    finally:
        if driver:
            driver.quit()


# ============================================================================
# EXAMPLE 5: Match Handling and Statistics
# ============================================================================

def example_5_match_handling():
    """
    Example 5: Demonstrate match handling and statistics tracking.
    
    Features:
    - Detect matches automatically
    - Handle match popups
    - Track match statistics
    - Report metrics
    
    This is most important for:
    - Verifying bot effectiveness
    - Monitoring account health
    - Detecting issues early
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Match Handling and Statistics".center(70))
    print("="*70 + "\n")
    
    print("[FEATURE] Match Detection and Handling\n")
    
    print("How matches work:")
    print("1. You swipe right on someone")
    print("2. They swipe right on you")
    print("3. Tinder detects mutual like")
    print("4. Match popup appears")
    print("5. Bot closes popup and continues\n")
    
    # Simulate statistics tracking
    stats = TinderStats()
    
    # Simulate swipes
    print("[SIMULATION] Simulating swipe statistics...\n")
    
    for i in range(20):
        if i % 3 == 0:
            stats.record_swipe("right")
            print(f"Swipe {i+1}: RIGHT (Like)")
        else:
            stats.record_swipe("left")
            print(f"Swipe {i+1}: LEFT (Pass)")
    
    # Simulate a match
    print("\n[MATCH] Match detected! Recording...")
    stats.record_match()
    print("Match recorded and popup handled.\n")
    
    # Report statistics
    stats.end_session(20)
    stats.print_summary()
    
    print("[METRICS]")
    print(f"Right/Left Ratio: {stats.stats['right_swipes']/stats.stats['left_swipes']:.2f}")
    print(f"Match Rate: {(stats.stats['matches']/stats.stats['total_swipes'])*100:.2f}%")
    print(f"Est. Matches per 100 Swipes: {(stats.stats['matches']/stats.stats['total_swipes'])*100:.1f}")
    print()


# ============================================================================
# EXAMPLE 6: Error Recovery and Resilience
# ============================================================================

def example_6_error_recovery():
    """
    Example 6: Demonstrate error handling and recovery.
    
    Scenarios:
    - Network timeout during swipe
    - Popup appears unexpectedly
    - Bot loses connection
    - Element not found
    
    Resilience Features:
    - Timeouts with fallbacks
    - Retry logic
    - Graceful degradation
    - Partial completion handling
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Recovery and Resilience".center(70))
    print("="*70 + "\n")
    
    print("[FEATURE] Error Handling Strategies\n")
    
    print("Common errors and recovery:\n")
    
    print("1. TIMEOUT ERROR")
    print("   Problem: Element not found within time limit")
    print("   Solution: Use fallback mechanism")
    print("   Code:")
    print("   try:")
    print("       button = WebDriverWait(driver, TIMEOUT).until(...)")
    print("   except TimeoutException:")
    print("       # Fallback: keyboard shortcut")
    print("       driver.send_keys(Keys.ARROW_RIGHT)\n")
    
    print("2. STALE ELEMENT ERROR")
    print("   Problem: Element is no longer in DOM")
    print("   Solution: Re-find element")
    print("   Code:")
    print("   element = driver.find_element(...)  # Find again")
    print("   element.click()\n")
    
    print("3. NETWORK ERROR")
    print("   Problem: Connection fails during action")
    print("   Solution: Retry with exponential backoff")
    print("   Code:")
    print("   for attempt in range(3):")
    print("       try:")
    print("           perform_action()")
    print("           break")
    print("       except NetworkError:")
    print("           time.sleep(2 ** attempt)\n")
    
    print("4. UNEXPECTED POPUP")
    print("   Problem: Popup appears instead of swipe")
    print("   Solution: Detect and handle")
    print("   Code:")
    print("   if check_for_match(driver):")
    print("       handle_match_popup(driver)\n")
    
    print("5. PARTIAL COMPLETION")
    print("   Problem: Swipe starts but network fails")
    print("   Solution: Record what succeeded, retry failed")
    print("   Code:")
    print("   successful_swipes = 0")
    print("   for swipe in swipes:")
    print("       try:")
    print("           perform_swipe()")
    print("           successful_swipes += 1")
    print("       except:")
    print("           continue\n")
    
    print("[BEST PRACTICE]")
    print("Always use try/except with specific exceptions")
    print("Have fallback mechanisms for each action")
    print("Log errors for debugging")
    print("Allow partial completion and retries")
    print()


# ============================================================================
# Main Menu
# ============================================================================

def main():
    """Display examples menu."""
    
    print()
    print("="*70)
    print("Day 50 - Tinder Bot Examples".center(70))
    print("="*70)
    print("""
Choose an example to run:

1. Simple Swiping Campaign
   └─ Basic workflow: login → swipe → statistics
   
2. Batch Swiping with Daily Limit
   └─ Respect Tinder's 100 swipes/day limit
   
3. Like-All Strategy
   └─ Swipe right on all profiles (maximize matches)
   
4. Selective Swiping Strategy
   └─ Only like ~30% (be choosy)
   
5. Match Handling and Statistics
   └─ Detect matches, track statistics
   
6. Error Recovery and Resilience
   └─ Handle errors gracefully
   
0. Show This Menu

⚠️  IMPORTANT REMINDERS:
- NEVER hardcode credentials (use environment variables)
- Test on real account at your own risk
- Read Tinder ToS before using
- Be ethical and transparent
- Use responsibly
    """)
    
    print("\nGETTING STARTED")
    print("-" * 70)
    print("""
1. Set up credentials securely:
   import os
   email = os.environ.get('FACEBOOK_EMAIL')
   password = os.environ.get('FACEBOOK_PASSWORD')

2. Choose a strategy:
   - Like-all (get more matches)
   - Selective (be choosy)
   - Mixed (balanced approach)

3. Respect limits:
   - Free: 100 swipes/day
   - Premium: More unlimited
   - Don't try to bypass

4. Monitor statistics:
   - Track swipes and matches
   - Watch for account flags
   - Adjust strategy as needed

5. Be ethical:
   - Inform your partner
   - Be genuine in profiles
   - Respect other users
    """)
    
    print("="*70)
    print("Examples ready!".center(70))
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
    
    # Uncomment example(s) to run:
    # example_1_simple_swiping()
    # example_2_batch_with_limit()
    # example_3_like_all_strategy()
    # example_4_selective_strategy()
    example_5_match_handling()  # This one has no real bot, just demo
    # example_6_error_recovery()
    
    print("\nTo run other examples, uncomment their function calls above.")
    print("Then run: python example_usage.py\n")
