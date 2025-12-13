# Day 51 - Complaining Twitter Bot with Speed Testing

Build an automated internet speed testing bot that complains to your ISP about poor speeds via Twitter when speeds fall below promised levels.

## Project Overview

### The Real-World Problem

Internet Service Providers (ISPs) frequently promise speeds they fail to deliver:

**Example Scenario:**
- Promised: 150 Mbps download, 10 Mbps upload
- Actual: 23 Mbps download, 5 Mbps upload
- Performance: Only 15% of promised speeds
- Contract says you pay for speeds you don't receive

**Why This Happens:**
- Network oversubscription (too many users per line)
- Aging infrastructure not upgraded
- Peak hour congestion (evenings, weekends)
- No enforcement of speed guarantees
- Customer service designed to discourage complaints

### Why Twitter Works

**Traditional Methods Don't Work:**
- ☓ Call customer service: 30+ minute waits, frustrated reps
- ☓ Email support: Ignored or slow 1-week responses
- ☓ Write to management: Bureaucratic delays
- ☓ File complaints: No action or token gestures

**Why Twitter Is Effective:**
- ✓ Public visibility (everyone sees your complaint)
- ✓ Social media monitoring (companies respond faster)
- ✓ Brand reputation concerns (company cares about image)
- ✓ Dedicated support teams (Twitter@comcastcares exists)
- ✓ Creates accountability (permanent public record)
- ✓ Precedent: Many users successfully obtained refunds

### Real-World Success Stories

**Documented Cases:**
1. **Comcast User:** Posted Twitter complaint with speed test data → Received $50/month credit + service upgrade
2. **AT&T Customer:** Tweeted consistent 30% speed shortfalls → Got service tier upgrade
3. **BT User (UK):** Twitter complaint thread → Full month refund
4. **Spectrum Customer:** Regular tweets with data → Negotiated lower rate

**Why Companies Respond:**
- Public complaints damage reputation
- Other customers see the issue
- Competitor mentions attract attention
- Social media teams have authority
- Faster resolution = fewer complaints

## How the Bot Works

### Complete Workflow

```
1. SPEED TESTING
   └─ Selenium opens speedtest.net
   └─ Clicks "Go" button
   └─ Waits 1-2 minutes
   └─ Extracts results (download, upload, ping)

2. SPEED COMPARISON
   └─ Compares actual vs promised speeds
   └─ Calculates % of promised speed
   └─ Determines if acceptable (threshold: 80%)

3. COMPLAINT GENERATION
   └─ Creates witty, factual complaint
   └─ Includes ISP handle
   └─ Provides specific data
   └─ Keeps under 280 characters

4. TWITTER POSTING
   └─ Uses Twitter API to post tweet
   └─ Mentions ISP support handle
   └─ Creates public record
   └─ Builds accountability

5. RESULT TRACKING
   └─ Saves to JSON file
   └─ Tracks history over time
   └─ Shows patterns
   └─ Provides evidence for disputes
```

### Key Features

✓ **Automated Speed Testing** - Selenium controls speedtest.net  
✓ **ISP Configuration** - Pre-configured for major ISPs  
✓ **Speed Analysis** - Compares actual vs promised  
✓ **Tweet Generation** - Creates professional complaints  
✓ **Twitter Integration** - Posts via official API  
✓ **Result Tracking** - Maintains historical data  
✓ **Error Handling** - Retries on network failures  
✓ **Ethical Guidelines** - Truthful complaints only  

## Technical Setup

### Installation

```bash
pip install selenium tweepy
```

### Chrome Driver

1. Download ChromeDriver from https://chromedriver.chromium.org/
2. Add to PATH or specify in code
3. Ensure version matches Chrome browser version

### Twitter API Setup

1. Go to https://developer.twitter.com/
2. Create Developer Account
3. Create New App (Project)
4. Generate API keys and tokens in API Keys & Tokens tab

**Credentials Needed:**
- API Key
- API Key Secret
- Access Token
- Access Token Secret

**Set Environment Variables:**

```bash
# Windows Command Prompt
set TWITTER_API_KEY=your_key_here
set TWITTER_API_SECRET=your_secret_here
set TWITTER_ACCESS_TOKEN=your_token_here
set TWITTER_ACCESS_SECRET=your_secret_here

# Windows PowerShell
$env:TWITTER_API_KEY="your_key_here"
$env:TWITTER_API_SECRET="your_secret_here"
$env:TWITTER_ACCESS_TOKEN="your_token_here"
$env:TWITTER_ACCESS_SECRET="your_secret_here"

# Linux/Mac
export TWITTER_API_KEY="your_key_here"
export TWITTER_API_SECRET="your_secret_here"
export TWITTER_ACCESS_TOKEN="your_token_here"
export TWITTER_ACCESS_SECRET="your_secret_here"
```

### ISP Configuration

Update promised speeds in code or config:

```python
run_speed_complaint_bot(
    isp_key="comcast",      # ISP identifier
    promised_down=150,       # Promised download (Mbps)
    promised_up=10,          # Promised upload (Mbps)
    should_tweet=False       # Post to Twitter?
)
```

## Supported ISPs

Pre-configured providers:

| ISP | Handle | Key |
|-----|--------|-----|
| Comcast | @comcastcares | comcast |
| AT&T | @ATTCares | att |
| Verizon | @VerizonSupport | verizon |
| Charter Spectrum | @SpectrumSupport | spectrum |
| Sky (UK) | @SkyHelp | sky |
| BT (UK) | @BTCare | bt |

**Adding New ISP:**

```python
ISP_CONFIGS["myisp"] = {
    "name": "My ISP",
    "handle": "@MySupportHandle",
    "typical_promises": {
        "plan_name": {"down": 100, "up": 10}
    }
}
```

## Usage Examples

### Basic Speed Test (No Twitter)

```python
from speed_complaint_bot import run_speed_complaint_bot

result = run_speed_complaint_bot(
    isp_key="comcast",
    promised_down=150,
    promised_up=10,
    should_tweet=False
)

# Check if speeds acceptable
if not result['comparison']['acceptable']:
    print(f"Poor speeds: {result['complaint']}")
```

### With Twitter Posting

```python
# Make sure TWITTER_API_* env vars are set first!
result = run_speed_complaint_bot(
    isp_key="comcast",
    promised_down=150,
    promised_up=10,
    should_tweet=True  # Post to Twitter
)
```

### View Result History

```python
from speed_complaint_bot import view_results_history

# Show last 10 tests
view_results_history(limit=10)
```

### Manual Speed Test

```python
from speed_complaint_bot import (
    setup_chrome_driver,
    run_speedtest,
    compare_speeds
)

driver = setup_chrome_driver(headless=False)
speeds = run_speedtest(driver)
driver.quit()

print(f"Download: {speeds['download']} Mbps")
print(f"Upload: {speeds['upload']} Mbps")
```

### Comparison Example

```python
from speed_complaint_bot import compare_speeds

actual = {"download": 23.5, "upload": 4.2}
promised = {"down": 150, "up": 10}

comparison = compare_speeds(actual, promised)
# {
#   "download_percent": 15.7,
#   "upload_percent": 42.0,
#   "acceptable": False,
#   "down_shortfall": 126.5
# }
```

## Core Functions

### Browser Setup
- `setup_chrome_driver(headless=False)` - Initialize WebDriver

### Speed Testing
- `run_speedtest(driver)` - Run test on speedtest.net, returns speeds

### Analysis
- `compare_speeds(actual, promised)` - Compare and analyze speeds
- `generate_complaint_tweet(isp, speeds, promised)` - Create tweet

### Twitter
- `post_tweet_to_twitter(tweet_text)` - Post to Twitter
- `save_result(result_data)` - Store result to JSON
- `view_results_history(limit=10)` - Display past results

### Main Workflow
- `run_speed_complaint_bot(isp_key, promised_down, promised_up, should_tweet)` - Complete workflow

## Understanding Speed Test Results

### Download Speed
- How fast you can retrieve data from the internet
- Most important for: browsing, streaming video, downloads
- Typical household needs: 25-100 Mbps

### Upload Speed
- How fast you can send data to the internet
- Important for: video calls, uploads, cloud backups
- Typical household needs: 5-10 Mbps

### Ping (Latency)
- Time for data to travel to server and back
- Important for: online gaming, video calls
- Lower is better (< 50ms is good)

### What "Acceptable" Means
- Generally 80%+ of promised speeds is acceptable
- Below 80% suggests ISP is underperforming
- Document multiple tests to show pattern

## Result Storage

Results saved to `speed_test_results.json`:

```json
{
  "isp": "comcast",
  "timestamp": "2024-11-25T14:30:00.123456",
  "speeds": {
    "download": 23.5,
    "upload": 4.2,
    "ping": "45",
    "result_url": "https://www.speedtest.net/result/..."
  },
  "promised": {
    "down": 150,
    "up": 10
  },
  "comparison": {
    "down_percent": 15.7,
    "up_percent": 42.0,
    "acceptable": false,
    "down_shortfall": 126.5,
    "up_shortfall": 5.8
  },
  "tweet": "@comcastcares I'm getting 23.5Mbps down, promised 150..."
}
```

## Best Practices

### 1. Test Consistently
- Test at least 2-3 times per week
- Test at different times (morning, evening, weekend)
- Test on wired connection (more accurate)
- Document the pattern

### 2. Be Factual
- Use only verified speedtest.net results
- State promised speeds from your contract
- Calculate percentage accurately
- Include specific numbers

### 3. Professional Tone
- Be firm but respectful
- Focus on resolution, not blame
- Avoid ALL CAPS or excessive punctuation
- Include contract reference

### 4. Strategic Timing
- Post during business hours (ISP monitoring)
- Space out tweets (not spam)
- Include data, not just complaints
- Follow up if no response

### 5. Manage Expectations
- Some ISPs respond quickly, others don't
- You may get offered credit instead of fix
- Persistent documentation helps
- Switch providers if not resolved

## Ethical Guidelines

### When to Use This Bot
✓ You have consistent documented speed issues  
✓ You've tried traditional complaint methods  
✓ You want to build evidence  
✓ ISP has failed to fix problems  
✓ You're comfortable with public tweets  

### DO This
✓ Use only truthful, verified speeds  
✓ Be professional and factual  
✓ Back up claims with data  
✓ Follow Twitter Terms of Service  
✓ Space out tweets reasonably  
✓ Research ISP's Twitter history  
✓ Document everything  

### DON'T Do This
✗ Fabricate or exaggerate speeds  
✗ Use for harassment or abuse  
✗ Spam ISP with constant tweets  
✗ Make false claims  
✗ Violate Twitter Terms of Service  
✗ Tweet from fake accounts  
✗ Engage in public shaming  

## Dealing with ISP Responses

### Common ISP Claims

| Claim | Reality |
|-------|---------|
| "Speeds not guaranteed" | They ARE promised in contract |
| "That's typical for your area" | Why pay for more then? |
| "Your WiFi is the problem" | Run on wired connection |
| "You need newer modem" | ISP provides modem |
| "Speeds vary throughout day" | So provide consistent speed |

### How to Respond
1. Have data (multiple tests)
2. Run tests wired, not WiFi
3. Reference your contract
4. Show historical trend
5. Stay professional
6. Ask for specific action (fix, credit, or cancel)

## Troubleshooting

### Speed Test Timeout
- Speedtest.net might be slow
- Your internet might be very slow
- Browser might be blocked by ISP
- Solution: Retry, wait longer, check browser

### Button Not Found
- Website layout changed
- JavaScript not loaded
- Solution: Try multiple CSS selectors, use JavaScript to click

### Twitter API Error
- Credentials not set correctly
- Tweepy not installed
- API rate limits exceeded
- Solution: Check env vars, install tweepy, wait before retrying

### Invalid Speed Results
- Test interrupted
- Website error
- Solution: Retry, ensure full test completion

## Scheduling the Bot

### Windows Task Scheduler
```batch
# Create scheduled task to run daily
python "C:\path\to\daily_speed_test.py"
```

### Linux Cron
```bash
# Run daily at 6 PM
0 18 * * * python /path/to/daily_speed_test.py
```

### Python Scheduler
```python
import schedule
import time
from speed_complaint_bot import run_speed_complaint_bot

def job():
    run_speed_complaint_bot(
        isp_key="comcast",
        promised_down=150,
        promised_up=10,
        should_tweet=False  # Set to True after testing
    )

schedule.every().day.at("18:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Key Takeaways

✅ **Automation:** Selenium automates speedtest.net testing  
✅ **API Integration:** Twitter API posts complaints  
✅ **Data Analysis:** Compare actual vs promised speeds  
✅ **Public Accountability:** Leverage Twitter for better service  
✅ **Evidence Building:** Historical data strengthens claims  
✅ **Ethical Automation:** Truthful, professional complaints  

## Project Extensions

### Basic
- [x] Run speed test
- [x] Compare speeds
- [x] Generate tweet
- [x] Track results

### Intermediate
- [ ] Schedule bot to run daily
- [ ] Email notifications on poor speeds
- [ ] Multiple ISP testing
- [ ] Automatic escalation

### Advanced
- [ ] Dashboard showing trends
- [ ] Multi-provider comparison
- [ ] Automatic retry on poor speeds
- [ ] Predictive analysis
- [ ] Report generation

### Production
- [ ] Persistent logging
- [ ] Error monitoring
- [ ] Database storage
- [ ] Web dashboard
- [ ] Mobile alerts
- [ ] Community data sharing

## Real-World Impact

**How Public Complaints Work:**

1. **Visibility** - Everyone sees your complaint
2. **Pressure** - Other users ReTweet/Like
3. **Response** - Company social team monitors Twitter
4. **Resolution** - Faster service than traditional methods
5. **Evidence** - Public record of problem
6. **Leverage** - Use for refunds or escalation

**Success Metrics:**
- Company responds within 24 hours
- Gets transferred to technical team
- Receives credit or service upgrade
- Issue eventually gets fixed
- Can cancel without penalty

## Summary

Day 51 demonstrates real-world automation solving a practical problem: holding ISPs accountable for promised speeds through data-backed public complaints on Twitter. The bot combines Selenium automation (speed testing) with Twitter API integration (complaint posting) to create an efficient system for consumer advocacy.

The project teaches important lessons about ethical automation, data analysis, and leveraging social media for consumer protection.

---

**Files in Project:**
- `main.py` - Overview and concepts
- `speed_complaint_bot.py` - Core implementation
- `example_usage.py` - Working examples
- `README.md` - This documentation
- `speed_test_results.json` - Historical results

**Quick Start:**
1. Review `main.py` for overview
2. Check `example_usage.py` for working code
3. Study `speed_complaint_bot.py` implementation
4. Set up Twitter API credentials
5. Run first speed test
6. Post first complaint tweet

Good luck holding your ISP accountable! 📊📱
