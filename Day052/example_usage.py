"""
Day 52 - Instagram Follower Bot Examples
Working code examples demonstrating how to use the bot

Each example is self-contained and ready to run.
Uncomment the examples you want to execute at the bottom.
"""

from instagram_follower_bot import (
    run_follower_bot,
    view_results_history,
    TARGET_ACCOUNTS,
    setup_chrome_driver,
    login_to_instagram,
    navigate_to_profile,
    open_followers_modal,
    follow_users_from_followers,
    save_results,
    logout_from_instagram,
)
import time


# ============================================================================
# EXAMPLE 1: Basic Following
# ============================================================================

def example_1_basic_following():
    """
    Example 1: Basic following workflow.
    
    Scenario: Follow 50 users from ChefSteps
    Time: ~5 minutes (with delays)
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Following".center(70))
    print("="*70 + "\n")
    
    try:
        result = run_follower_bot(
            instagram_username="your_username",  # Change this
            instagram_password="your_password",  # Change this
            target_account="chefsteps",
            num_follows=50,
            headless=False  # Show browser
        )
        
        print(f"\n✓ Successfully followed: {result['successful_follows']}")
        print(f"✓ Already following: {result['already_following']}")
        print(f"✗ Errors: {result['errors']}")
    
    except Exception as e:
        print(f"\n[ERROR] Example failed: {e}")
        print("[TIP] Check credentials and account restrictions")


# ============================================================================
# EXAMPLE 2: Different Target Account
# ============================================================================

def example_2_different_target():
    """
    Example 2: Follow from different account (Gordon Ramsay).
    
    Scenario: Different niche with celebrity chef
    Different audience: People interested in high-end cooking
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Different Target Account".center(70))
    print("="*70 + "\n")
    
    try:
        print("[TARGET] Using: Gordon Ramsay (@gordonramsay)")
        print("[AUDIENCE] Celebrity chef followers")
        print("[NICHE] High-end cooking and kitchen content\n")
        
        result = run_follower_bot(
            instagram_username="your_username",
            instagram_password="your_password",
            target_account="gordon_ramsay",  # Different account
            num_follows=50,
            headless=False
        )
        
        print(f"\n✓ Results: {result['successful_follows']} followed")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 3: Larger Batch
# ============================================================================

def example_3_larger_batch():
    """
    Example 3: Follow larger batch of users.
    
    Scenario: 300 follows in one session
    Time: ~30-40 minutes
    Includes batch pauses for rate limiting
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Larger Batch (300 Follows)".center(70))
    print("="*70 + "\n")
    
    try:
        print("[INFO] This will take 30-40 minutes")
        print("[INFO] Includes batch pauses every 50 follows")
        print("[INFO] Simulates human behavior\n")
        
        result = run_follower_bot(
            instagram_username="your_username",
            instagram_password="your_password",
            target_account="tasty",
            num_follows=300,  # Large batch
            headless=True  # No UI to speed up
        )
        
        print(f"\n✓ Total followed: {result['successful_follows']}")
        print(f"✓ Success rate: {result['successful_follows']}/{result['total_attempts']}")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 4: Multiple Accounts in Sequence
# ============================================================================

def example_4_multiple_accounts():
    """
    Example 4: Follow from multiple target accounts.
    
    Scenario: Diversify followers across 3 targets
    Strategy: Reach different audience segments
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Multiple Target Accounts".center(70))
    print("="*70 + "\n")
    
    targets = ["chefsteps", "gordon_ramsay", "tasty"]
    total_followed = 0
    
    try:
        for target in targets:
            print(f"\n[TARGET] Working on: @{target}")
            print("[INFO] Following 50 users...\n")
            
            result = run_follower_bot(
                instagram_username="your_username",
                instagram_password="your_password",
                target_account=target,
                num_follows=50,
                headless=True
            )
            
            total_followed += result['successful_follows']
            print(f"✓ This target: {result['successful_follows']} followed")
            
            # Wait between accounts
            print("\n[WAIT] Waiting 5 minutes before next account...")
            for i in range(5, 0, -1):
                print(f"\r  {i} minutes remaining...", end="")
                time.sleep(60)
            print()
        
        print(f"\n[TOTAL] All targets complete: {total_followed} total followed")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 5: View Results History
# ============================================================================

def example_5_view_history():
    """
    Example 5: Display historical results.
    
    Scenario: Review past bot sessions
    Use case: Track growth and metrics
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: View Results History".center(70))
    print("="*70 + "\n")
    
    print("[INFO] Displaying last 10 sessions\n")
    
    view_results_history(limit=10)
    
    print("\n[FILE] Results saved to: follower_bot_results.json")
    print("[TIP] Use to track:")
    print("  • Follow-back rates")
    print("  • Success patterns")
    print("  • Best target accounts")


# ============================================================================
# EXAMPLE 6: Headless Mode (No UI)
# ============================================================================

def example_6_headless_mode():
    """
    Example 6: Run bot without browser window.
    
    Scenario: Background automation
    Use case: Scheduled/automated running
    Benefit: Faster, less resource usage
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Headless Mode (No UI)".center(70))
    print("="*70 + "\n")
    
    try:
        print("[MODE] Running in headless mode (no browser window)")
        print("[BENEFIT] Faster, less CPU usage")
        print("[USE] Perfect for scheduled tasks\n")
        
        result = run_follower_bot(
            instagram_username="your_username",
            instagram_password="your_password",
            target_account="seriouseats",
            num_follows=100,
            headless=True  # No UI window
        )
        
        print(f"\n✓ Results: {result['successful_follows']} followed")
        print("[INFO] Bot ran silently in background")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 7: Custom Workflow Control
# ============================================================================

def example_7_custom_workflow():
    """
    Example 7: Advanced workflow with manual control.
    
    Scenario: Control each step separately
    Use case: Debugging, custom logic, monitoring
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Custom Workflow Control".center(70))
    print("="*70 + "\n")
    
    driver = None
    
    try:
        print("[STEP 1] Setting up browser...")
        driver = setup_chrome_driver(headless=False, profile_name="custom_profile")
        
        print("[STEP 2] Logging in...")
        login_to_instagram(driver, "your_username", "your_password")
        
        print("[STEP 3] Navigating to profile...")
        navigate_to_profile(driver, "chefsteps")
        
        print("[STEP 4] Opening followers...")
        open_followers_modal(driver)
        
        print("[STEP 5] Following users...")
        stats = follow_users_from_followers(driver, count=75)
        
        print(f"\n✓ Results: {stats['successful_follows']} followed")
        
        print("[STEP 6] Saving results...")
        save_results("chefsteps", stats)
        
        print("[STEP 7] Logging out...")
        logout_from_instagram(driver)
        
        print("\n✓ Workflow complete!")
    
    except Exception as e:
        print(f"[ERROR] Workflow failed: {e}")
    
    finally:
        if driver:
            driver.quit()
            print("[CLEANUP] Browser closed")


# ============================================================================
# EXAMPLE 8: Available Target Accounts
# ============================================================================

def example_8_view_targets():
    """
    Example 8: View all available target accounts.
    
    Scenario: See what accounts are preconfigured
    Use case: Choose best targets for your niche
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Available Target Accounts".center(70))
    print("="*70 + "\n")
    
    print("[ACCOUNTS] Pre-configured targets:\n")
    
    for key, config in TARGET_ACCOUNTS.items():
        print(f"  Key: {key:<15} | @{config['username']:<20}")
        print(f"    Category: {config['category']}")
        print(f"    Description: {config['description']}")
        print()
    
    print("[TIP] How to choose:")
    print("  1. Match your niche (cooking → ChefSteps)")
    print("  2. Followers = your target audience")
    print("  3. High follow-back rate (15-30%)")
    print("  4. Active, engaged followers")
    print()
    print("[CUSTOM] To add more targets:")
    print("  1. Edit TARGET_ACCOUNTS in instagram_follower_bot.py")
    print("  2. Add username and category")
    print("  3. Use in run_follower_bot() calls")


# ============================================================================
# EXAMPLE 9: Growth Strategy Analysis
# ============================================================================

def example_9_growth_strategy():
    """
    Example 9: Analyze growth strategy effectiveness.
    
    Scenario: Calculate metrics and ROI
    Use case: Optimize and track progress
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: Growth Strategy Analysis".center(70))
    print("="*70 + "\n")
    
    print("[STRATEGY] Recommended Daily Schedule:\n")
    
    schedule = [
        ("Morning (6 AM)", "ChefSteps", 100),
        ("Midday (12 PM)", "Gordon Ramsay", 100),
        ("Evening (6 PM)", "Tasty", 100),
    ]
    
    total_daily = 0
    estimated_followback = 0
    
    for time_slot, account, follows in schedule:
        followback = follows * 0.20  # 20% follow-back rate
        total_daily += follows
        estimated_followback += followback
        
        print(f"{time_slot:<20} @{account:<20} {follows} follows")
        print(f"  {'└─ Estimated':<18} {followback:.0f} follow-backs\n")
    
    print(f"[DAILY] Total: {total_daily} follows")
    print(f"[DAILY] Est. follow-backs: {estimated_followback:.0f}")
    print()
    print(f"[WEEKLY] {total_daily * 7} follows")
    print(f"[WEEKLY] Est. followers gained: {estimated_followback * 7:.0f}")
    print()
    print(f"[MONTHLY] {total_daily * 30} follows")
    print(f"[MONTHLY] Est. followers gained: {estimated_followback * 30:.0f}")
    print()
    print("[IMPORTANT] Keep in mind:")
    print("  • Post high-quality content regularly")
    print("  • Engage with followers' content")
    print("  • Maintain niche relevance")
    print("  • Monitor for account restrictions")


# ============================================================================
# EXAMPLE 10: Safety Check Before First Run
# ============================================================================

def example_10_safety_check():
    """
    Example 10: Pre-flight safety checks.
    
    Scenario: Verify everything before running
    Use case: Avoid common mistakes
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: Pre-Flight Safety Checks".center(70))
    print("="*70 + "\n")
    
    print("[CHECK 1] Instagram Account")
    print("  ☐ Username and password ready")
    print("  ☐ Email verified")
    print("  ☐ 2FA disabled (temporary)")
    print("  ☐ Account at least 1 day old")
    print("  ☐ No pending restrictions")
    print()
    
    print("[CHECK 2] System Setup")
    print("  ☐ Selenium installed (pip install selenium)")
    print("  ☐ ChromeDriver downloaded")
    print("  ☐ ChromeDriver in PATH or project folder")
    print("  ☐ Chrome browser installed")
    print()
    
    print("[CHECK 3] Target Account Selection")
    print("  ☐ Target matches your niche")
    print("  ☐ Target has 100k+ followers")
    print("  ☐ Target is real, not bot account")
    print("  ☐ Target posts regularly")
    print()
    
    print("[CHECK 4] Bot Configuration")
    print("  ☐ Rate limiting settings configured")
    print("  ☐ Batch size appropriate")
    print("  ☐ Delays set conservatively")
    print("  ☐ Max follows per session limited")
    print()
    
    print("[CHECK 5] Initial Test")
    print("  ☐ Run with small batch (25 follows)")
    print("  ☐ Watch browser for errors")
    print("  ☐ Verify follows in history")
    print("  ☐ Check for Instagram warnings")
    print()
    
    print("[TIP] If all checks pass, you're ready!")
    print("[CAUTION] Start small, scale gradually")
    print("[MONITOR] Watch account for first 24 hours")


# ============================================================================
# Main Menu
# ============================================================================

def main():
    """Display examples menu and instructions."""
    
    print()
    print("="*70)
    print("Day 52 - Instagram Follower Bot Examples".center(70))
    print("="*70)
    print("""
Choose an example to run or uncomment below:

1. Basic Following (50 from ChefSteps)
2. Different Target (Gordon Ramsay followers)
3. Larger Batch (300 follows in one session)
4. Multiple Accounts (diversified followers)
5. View History (see past bot sessions)
6. Headless Mode (no browser window)
7. Custom Workflow (manual control)
8. View Targets (available accounts)
9. Growth Strategy (analysis and projections)
10. Safety Check (pre-flight verification)

QUICK START:
──────────────────────────────────────────────────────────────────────

1. Uncomment Example 10: Safety Check
2. Verify all checks pass
3. Uncomment Example 1: Basic Following
4. Edit credentials (your_username, your_password)
5. Uncomment and run
6. Monitor browser during execution

IMPORTANT REMINDERS:
──────────────────────────────────────────────────────────────────────

✓ FIRST TIME: Use small batch (50) with headless=False
✓ WATCH CAREFULLY: Check for errors and Instagram messages
✓ CREDENTIALS: Edit examples with real username/password
✓ RATE LIMITS: Don't exceed 300 per session
✓ BREAKS: Take 24-48 hour breaks between sessions
✓ CONTENT: Post regularly to keep followers engaged

RUNNING EXAMPLES:
──────────────────────────────────────────────────────────────────────

Option A - Direct:
    python example_usage.py
    # Runs main() with instructions

Option B - Uncomment:
    1. Edit this file
    2. Find function at bottom
    3. Uncomment the function call
    4. Run: python example_usage.py

Option C - Import:
    from example_usage import example_1_basic_following
    example_1_basic_following()

TROUBLESHOOTING:
──────────────────────────────────────────────────────────────────────

Error: "chromedriver not found"
  → Download from chromedriver.chromium.org
  → Place in C:\\Windows or project folder

Error: "Login failed"
  → Verify credentials (uppercase/lowercase matters)
  → Check for 2FA (must disable for bot)
  → Verify account not restricted

Error: "Followers modal won't open"
  → Try different target account
  → Check Instagram isn't updated
  → See troubleshooting in README.md
    """)
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
    
    # Uncomment example(s) to run:
    # example_1_basic_following()
    # example_2_different_target()
    # example_3_larger_batch()
    # example_4_multiple_accounts()
    # example_5_view_history()
    # example_6_headless_mode()
    # example_7_custom_workflow()
    # example_8_view_targets()
    # example_9_growth_strategy()
    # example_10_safety_check()
    
    print("To run an example:")
    print("1. Uncomment function call above")
    print("2. Run: python example_usage.py\n")
