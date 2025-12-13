"""
Day 51 - Speed Test Twitter Bot Examples
Working code examples demonstrating how to use the bot

Each example is self-contained and ready to run.
Uncomment the examples you want to run at the bottom of the file.
"""

from speed_complaint_bot import (
    setup_chrome_driver,
    run_speedtest,
    compare_speeds,
    generate_complaint_tweet,
    post_tweet_to_twitter,
    save_result,
    view_results_history,
    run_speed_complaint_bot,
    ISP_CONFIGS,
)
import time


# ============================================================================
# EXAMPLE 1: Basic Speed Test Only
# ============================================================================

def example_1_basic_speed_test():
    """
    Example 1: Run a speed test without tweeting.
    
    Scenario: You just want to test your speeds
    Result: Get download, upload, ping results
    Time: ~2-3 minutes
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Speed Test".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        print("[SETUP] Starting browser...")
        driver = setup_chrome_driver(headless=False)
        
        print("\n[TEST] Running speed test on speedtest.net...")
        print("[INFO] This will take 1-2 minutes\n")
        
        speeds = run_speedtest(driver)
        
        print("\n[RESULTS] Speed Test Complete:")
        print(f"  Download: {speeds['download']:.2f} Mbps")
        print(f"  Upload: {speeds['upload']:.2f} Mbps")
        print(f"  Ping: {speeds['ping']}")
        print(f"  Result URL: {speeds['result_url']}")
        
        return speeds
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")
        return None
    
    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()
            print("[OK] Done!\n")


# ============================================================================
# EXAMPLE 2: Speed Test with Comcast Complaint
# ============================================================================

def example_2_comcast_complaint():
    """
    Example 2: Test speeds and generate Comcast complaint (no tweet).
    
    Scenario: You pay for 150 Mbps from Comcast
    Expected: Compare vs actual and generate complaint
    
    Note: No tweeting in this example. Set should_tweet=True to post.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Comcast Speed Complaint Generation".center(70))
    print("="*70 + "\n")
    
    try:
        print("[CONFIG] ISP: Comcast")
        print("[CONFIG] Promised: 150 Mbps down / 10 Mbps up")
        print("[CONFIG] Tweet after: No (set should_tweet=True to post)\n")
        
        result = run_speed_complaint_bot(
            isp_key="comcast",
            promised_down=150,
            promised_up=10,
            should_tweet=False  # Don't post, just generate
        )
        
        if result:
            print("\n[RESULT] Bot completed successfully")
            if result.get('tweet'):
                print(f"\n[TWEET] Generated complaint:")
                print(f'"{result["tweet"]}"')
            else:
                print("\n[INFO] Speeds were acceptable, no complaint generated")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 3: Different ISP (AT&T)
# ============================================================================

def example_3_different_isp():
    """
    Example 3: Test and complain to different ISP (AT&T).
    
    Scenario: AT&T customer paying for 100 Mbps
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Different ISP (AT&T)".center(70))
    print("="*70 + "\n")
    
    try:
        print("[CONFIG] ISP: AT&T")
        print("[CONFIG] Promised: 100 Mbps down / 10 Mbps up\n")
        
        result = run_speed_complaint_bot(
            isp_key="att",
            promised_down=100,
            promised_up=10,
            should_tweet=False
        )
        
        if result:
            comparison = result.get('comparison', {})
            print(f"\n[ANALYSIS]")
            print(f"  Download: {comparison.get('down_percent', 0):.1f}% of promised")
            print(f"  Upload: {comparison.get('up_percent', 0):.1f}% of promised")
            print(f"  Status: {'✓ Acceptable' if comparison.get('acceptable') else '✗ Poor'}")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 4: Speed History
# ============================================================================

def example_4_view_history():
    """
    Example 4: View historical speed test results.
    
    Scenario: Review past speed tests
    Shows: Last 10 tests with timestamps and speeds
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: View Speed Test History".center(70))
    print("="*70 + "\n")
    
    try:
        print("[HISTORY] Displaying speed test results...\n")
        view_results_history(limit=10)
        
        print("\n[INFO] Results stored in: speed_test_results.json")
        print("[INFO] Each result includes speeds, ISP, timestamp, and tweet")
    
    except Exception as e:
        print(f"[ERROR] Example failed: {e}")


# ============================================================================
# EXAMPLE 5: Manual Speed Comparison
# ============================================================================

def example_5_manual_comparison():
    """
    Example 5: Manually compare speeds without full bot.
    
    Scenario: Use pre-measured speeds for comparison
    Use Case: Analyze previous test results
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Manual Speed Comparison".center(70))
    print("="*70 + "\n")
    
    # Simulate test results
    actual_speeds = {
        "download": 23.5,
        "upload": 4.2,
        "ping": "45"
    }
    
    promised_speeds = {
        "down": 150,
        "up": 10
    }
    
    print("[SPEEDS] Actual Results:")
    print(f"  Download: {actual_speeds['download']} Mbps")
    print(f"  Upload: {actual_speeds['upload']} Mbps")
    
    print("\n[PROMISED] From Contract:")
    print(f"  Download: {promised_speeds['down']} Mbps")
    print(f"  Upload: {promised_speeds['up']} Mbps")
    
    # Compare
    print("\n[ANALYZE] Comparing speeds...")
    comparison = compare_speeds(actual_speeds, promised_speeds)
    
    print(f"\n[RESULT] Analysis:")
    print(f"  Download: {comparison['down_percent']:.1f}% of promised")
    print(f"  Upload: {comparison['up_percent']:.1f}% of promised")
    print(f"  Status: {'✓ Acceptable' if comparison['acceptable'] else '✗ Poor'}")
    print(f"  Download Shortfall: {comparison['down_shortfall']:.1f} Mbps")
    print(f"  Upload Shortfall: {comparison['up_shortfall']:.1f} Mbps")
    
    # Generate complaint
    print("\n[TWEET] Generating complaint tweet...")
    tweet = generate_complaint_tweet(
        "Comcast",
        "@comcastcares",
        actual_speeds,
        promised_speeds
    )


# ============================================================================
# EXAMPLE 6: Tweet Generation Only
# ============================================================================

def example_6_tweet_generation():
    """
    Example 6: Generate complaint tweets for different scenarios.
    
    Scenario: See what complaint tweets would look like
    Use Case: Review before actual tweeting
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Tweet Generation Scenarios".center(70))
    print("="*70 + "\n")
    
    scenarios = [
        {
            "isp_name": "Comcast",
            "isp_handle": "@comcastcares",
            "actual": {"download": 23.5, "upload": 4.2, "ping": "45"},
            "promised": {"down": 150, "up": 10}
        },
        {
            "isp_name": "AT&T",
            "isp_handle": "@ATTCares",
            "actual": {"download": 45.2, "upload": 3.8, "ping": "55"},
            "promised": {"down": 100, "up": 10}
        },
        {
            "isp_name": "Verizon",
            "isp_handle": "@VerizonSupport",
            "actual": {"download": 78.5, "upload": 9.2, "ping": "25"},
            "promised": {"down": 100, "up": 10}
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nSCENARIO {i}: {scenario['isp_name']}")
        print("-" * 70)
        print(f"Promised: {scenario['promised']['down']}↓ / {scenario['promised']['up']}↑ Mbps")
        print(f"Actual:   {scenario['actual']['download']:.1f}↓ / {scenario['actual']['upload']:.1f}↑ Mbps")
        
        comparison = compare_speeds(scenario['actual'], scenario['promised'])
        
        print(f"\nStatus: {'✓ ACCEPTABLE' if comparison['acceptable'] else '✗ POOR'}")
        
        if not comparison['acceptable']:
            tweet = generate_complaint_tweet(
                scenario['isp_name'],
                scenario['isp_handle'],
                scenario['actual'],
                scenario['promised']
            )


# ============================================================================
# EXAMPLE 7: Multiple ISP Monitoring
# ============================================================================

def example_7_multiple_isps():
    """
    Example 7: Demonstrate different ISP configurations.
    
    Scenario: See what ISPs are supported
    Use Case: Choose which ISP to test
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Supported ISP Configurations".center(70))
    print("="*70 + "\n")
    
    print("[ISPs] Available ISP configurations:\n")
    
    for key, config in ISP_CONFIGS.items():
        print(f"Key: {key}")
        print(f"  Name: {config['name']}")
        print(f"  Twitter: {config['handle']}")
        print(f"  Typical Plans:")
        
        for plan_name, speeds in config['typical_promises'].items():
            print(f"    - {plan_name}: {speeds['down']}↓ / {speeds['up']}↑ Mbps")
        print()
    
    print("[INFO] To test an ISP:")
    print("""
    run_speed_complaint_bot(
        isp_key="att",  # Use key from above
        promised_down=100,
        promised_up=10,
        should_tweet=False
    )
    """)


# ============================================================================
# EXAMPLE 8: Complete Workflow (No Twitter)
# ============================================================================

def example_8_complete_workflow():
    """
    Example 8: Complete bot workflow from start to finish.
    
    Scenario: Full automated process without tweeting
    Shows: All major steps
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Complete Bot Workflow (No Twitter)".center(70))
    print("="*70 + "\n")
    
    print("[START] Beginning automated speed test workflow\n")
    
    print("STEP 1: Configure Bot")
    print("-" * 70)
    isp_key = "comcast"
    promised_down = 150
    promised_up = 10
    print(f"ISP: Comcast")
    print(f"Promised: {promised_down}↓ / {promised_up}↑ Mbps")
    print(f"Tweet: No (Demo mode)")
    
    print("\nSTEP 2: Run Speed Test")
    print("-" * 70)
    print("This would:")
    print("  - Open speedtest.net in browser")
    print("  - Click 'Go' button")
    print("  - Wait 1-2 minutes for test")
    print("  - Extract results")
    print("  - Close browser")
    
    print("\nSTEP 3: Analyze Results")
    print("-" * 70)
    print("Example results:")
    actual = {"download": 23.5, "upload": 4.2}
    promised = {"down": 150, "up": 10}
    print(f"  Download: {actual['download']:.1f} / {promised['down']} Mbps")
    print(f"  Upload: {actual['upload']:.1f} / {promised['up']} Mbps")
    
    comparison = compare_speeds(actual, promised)
    print(f"\n  Analysis: Only {comparison['down_percent']:.1f}% of promised speeds")
    
    print("\nSTEP 4: Generate Complaint")
    print("-" * 70)
    if not comparison['acceptable']:
        tweet = generate_complaint_tweet(
            "Comcast",
            "@comcastcares",
            actual,
            promised
        )
    
    print("\nSTEP 5: Save Results")
    print("-" * 70)
    print("Results would be saved to: speed_test_results.json")
    print("Including: speeds, promised speeds, comparison, tweet, timestamp")
    
    print("\nSTEP 6: Ready to Tweet")
    print("-" * 70)
    print("To actually post tweet, set: should_tweet=True")
    print("First, ensure Twitter API credentials are configured:")
    print("  TWITTER_API_KEY")
    print("  TWITTER_API_SECRET")
    print("  TWITTER_ACCESS_TOKEN")
    print("  TWITTER_ACCESS_SECRET")
    
    print("\n[READY] Workflow complete!")


# ============================================================================
# Main Menu
# ============================================================================

def main():
    """Display examples menu."""
    
    print()
    print("="*70)
    print("Day 51 - Speed Test Twitter Bot Examples".center(70))
    print("="*70)
    print("""
Choose an example to run or uncomment at bottom:

1. Basic Speed Test Only
   └─ Just test speeds, no complaints

2. Comcast Speed Complaint
   └─ Test speeds and generate Comcast complaint

3. Different ISP (AT&T)
   └─ Test and complain to AT&T

4. View Speed History
   └─ Display past speed test results

5. Manual Speed Comparison
   └─ Analyze pre-measured speeds

6. Tweet Generation Examples
   └─ See sample complaint tweets

7. Supported ISPs
   └─ View available ISP configurations

8. Complete Workflow
   └─ Full process walkthrough (no actual twitter)

Each example is self-contained and copy-paste ready.
    """)
    
    print("RECOMMENDATIONS")
    print("-" * 70)
    print("""
Getting Started:
1. Run Example 7 first (view ISPs)
2. Try Example 5 (manual comparison)
3. Try Example 6 (tweet generation)
4. Try Example 4 (history)
5. Try Example 1 (basic speed test)

Advanced:
6. Try Example 2 (Comcast bot)
7. Try Example 3 (different ISP)
8. Try Example 8 (full workflow)

Production:
9. Set Twitter API credentials
10. Change should_tweet=True
11. Schedule bot to run daily
    """)
    
    print("RUNNING EXAMPLES")
    print("-" * 70)
    print("""
Option A - Direct:
    python example_usage.py
    # Runs examples selected in main()

Option B - Interactive:
    from example_usage import example_1_basic_speed_test
    example_1_basic_speed_test()

Option C - Uncomment:
    Uncomment examples at bottom, then:
    python example_usage.py
    """)
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
    
    # Uncomment any examples to run them:
    # example_1_basic_speed_test()
    # example_2_comcast_complaint()
    # example_3_different_isp()
    # example_4_view_history()
    # example_5_manual_comparison()
    # example_6_tweet_generation()
    # example_7_multiple_isps()
    # example_8_complete_workflow()
    
    print("To run an example, uncomment the function call above.")
    print("Then run: python example_usage.py\n")
