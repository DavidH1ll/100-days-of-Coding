# Day 92 - Amazon Canada Web Scraper

## Overview
Web scraper that parses Amazon search result HTML using BeautifulSoup. Extracts product title, price, rating, review count, and availability. Saves results to CSV. Uses a local sample HTML file for reliable testing.

## Features
- Parses Amazon search result cards
- Extracts title, price (whole + fraction), star rating, review count
- Detects availability status (In Stock, Unavailable)
- Exports structured data to CSV
- Regex-based rating extraction

## Key Concepts
- BeautifulSoup CSS selectors (select_one, select)
- HTML parsing with class-based element targeting
- Regex for extracting numeric values from text
- CSV export with DictWriter

## Reflection
Using a sample HTML file instead of live requests avoids the constant battle with Amazon's anti-bot measures. The real skill is writing resilient CSS selectors that handle missing elements gracefully — every field has a fallback to None or "N/A".

**Day 92 Complete!** ✅
