"""Day 36 - Stock News Monitor

Monitors stock price changes and sends alerts with relevant news when significant
fluctuations occur. Inspired by Bloomberg terminal functionality.

Usage:
  python main.py [--dry-run]

Environment variables (.env file):
  STOCK_SYMBOL, COMPANY_NAME, PRICE_CHANGE_THRESHOLD,
  ALPHA_VANTAGE_API_KEY, NEWS_API_KEY,
  TWILIO_* or EMAIL_* credentials, USE_SMS, DRY_RUN
"""
from __future__ import annotations

import os
import sys
from typing import Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from stock_api import get_stock_change
from news_api import fetch_news, format_articles
from notifications import send_notification, env_bool


def build_alert_message(stock_data: dict, news_summary: str) -> tuple[str, str]:
    """Build alert subject and body from stock data and news.
    
    Returns (subject, body) tuple.
    """
    symbol = stock_data["symbol"]
    direction = stock_data["direction"]
    change_pct = stock_data["abs_change_percent"]
    yesterday_close = stock_data["yesterday_close"]
    day_before_close = stock_data["day_before_close"]
    yesterday_date = stock_data["yesterday_date"]
    day_before_date = stock_data["day_before_date"]
    
    subject = f"{symbol}: {direction} {change_pct:.1f}% Price Change Alert"
    
    body_lines = [
        f"{symbol} Stock Alert",
        f"{direction} {change_pct:.2f}% change detected",
        "",
        f"Previous close ({day_before_date}): ${day_before_close:.2f}",
        f"Latest close ({yesterday_date}): ${yesterday_close:.2f}",
        f"Change: ${yesterday_close - day_before_close:+.2f}",
        "",
        "Recent News:",
        news_summary
    ]
    
    body = "\n".join(body_lines)
    
    return subject, body


def main(argv: list[str]) -> int:
    """Main entry point for stock monitoring."""
    dry_run = "--dry-run" in argv or env_bool("DRY_RUN", False)
    
    # Configuration
    symbol = os.getenv("STOCK_SYMBOL", "TSLA")
    company_name = os.getenv("COMPANY_NAME", "Tesla Inc")
    threshold = float(os.getenv("PRICE_CHANGE_THRESHOLD", "5.0"))
    alpha_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    news_key = os.getenv("NEWS_API_KEY")
    use_sms = env_bool("USE_SMS", False)
    max_articles = int(os.getenv("MAX_NEWS_ARTICLES", "3"))
    
    if not alpha_key:
        print("[ERROR] ALPHA_VANTAGE_API_KEY not set")
        return 2
    
    if not news_key:
        print("[ERROR] NEWS_API_KEY not set")
        return 2
    
    print(f"Monitoring {symbol} ({company_name})")
    print(f"Alert threshold: {threshold}%\n")
    
    # Fetch stock data
    print("Fetching stock data...")
    stock_data = get_stock_change(symbol, alpha_key)
    
    if not stock_data:
        print("[ERROR] Failed to fetch stock data")
        return 1
    
    change_pct = stock_data["abs_change_percent"]
    direction = stock_data["direction"]
    
    print(f"{symbol}: {direction} {change_pct:.2f}%")
    print(f"  {stock_data['day_before_date']}: ${stock_data['day_before_close']:.2f}")
    print(f"  {stock_data['yesterday_date']}: ${stock_data['yesterday_close']:.2f}\n")
    
    # Check if threshold exceeded
    if change_pct < threshold:
        print(f"✓ Price change ({change_pct:.2f}%) below threshold ({threshold}%)")
        print("No alert needed.")
        return 0
    
    print(f"⚠ Price change ({change_pct:.2f}%) exceeds threshold ({threshold}%)")
    print("Fetching news...\n")
    
    # Fetch news
    articles = fetch_news(company_name, news_key, days_back=3)
    
    if not articles:
        news_summary = "No recent news articles found."
    else:
        print(f"Found {len(articles)} articles")
        news_summary = format_articles(articles, max_count=max_articles)
    
    # Build alert message
    subject, body = build_alert_message(stock_data, news_summary)
    
    if dry_run:
        print("\n" + "="*60)
        print("DRY RUN - Alert Preview")
        print("="*60)
        print(f"Subject: {subject}")
        print(f"Method: {'SMS' if use_sms else 'Email'}")
        print("-"*60)
        print(body)
        print("="*60 + "\n")
        return 0
    
    # Send notification
    print(f"Sending alert via {'SMS' if use_sms else 'Email'}...")
    success = send_notification(subject, body, use_sms)
    
    if success:
        print("✅ Alert sent successfully!")
        return 0
    else:
        print("❌ Failed to send alert")
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
