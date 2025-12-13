# Day 45 - Web Scraping with BeautifulSoup

## Project Overview
Learn web scraping fundamentals using BeautifulSoup4, a powerful Python library for parsing HTML and extracting data from websites. This project demonstrates how to work with real-world web data when APIs are unavailable or insufficient.

## Learning Objectives
- Understand what web scraping is and when to use it
- Learn BeautifulSoup4 syntax and methods
- Parse HTML and extract specific elements
- Work with CSS selectors for more advanced queries
- Respect web scraping ethics and best practices
- Handle real-world web requests and errors

## What is BeautifulSoup?

BeautifulSoup is an HTML/XML parser that transforms messy, complex HTML code into a "soup" of organized data structures you can navigate and search through easily.

### Key Benefits:
- ✅ Parse and extract data from websites
- ✅ Navigate HTML structure intuitively
- ✅ Use multiple parsing backends
- ✅ Handle malformed HTML gracefully
- ✅ Works with both HTML and XML

## Project Contents

### main.py
A comprehensive guide with 4 practical examples:

1. **Example 1: Simple HTML Parsing**
   - Parse basic HTML strings
   - Extract text from elements
   - Work with classes and nested elements

2. **Example 2: Web Scraping from Real Websites**
   - Fetch web pages using requests library
   - Add user-agent headers to avoid blocking
   - Handle network errors gracefully

3. **Example 3: Local HTML Analysis**
   - Parse structured movie data
   - Extract nested elements
   - Organize data into dictionaries

4. **Example 4: Advanced Parsing with CSS Selectors**
   - Use CSS selector syntax
   - Use select() and select_one() methods
   - Extract complex nested structures

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Install Dependencies
```bash
pip install beautifulsoup4 requests
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to see all examples:
```bash
python main.py
```

### Basic Usage Example
```python
from bs4 import BeautifulSoup
import requests

# Fetch a webpage
response = requests.get('https://example.com')

# Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find elements
title = soup.find('h1').string
paragraphs = soup.find_all('p')

# Use CSS selectors
movies = soup.select('div.movie-item')
```

## BeautifulSoup Methods Reference

### Finding Elements

| Method | Description | Example |
|--------|-------------|---------|
| `find()` | Find first matching element | `soup.find('h1', class_='title')` |
| `find_all()` | Find all matching elements | `soup.find_all('p')` |
| `select()` | CSS selector (finds all) | `soup.select('div.movie')` |
| `select_one()` | CSS selector (finds first) | `soup.select_one('#main')` |

### Accessing Data

| Property/Method | Description | Example |
|-----------------|-------------|---------|
| `.string` | Get element's text | `element.string` |
| `.text` | Get all text (recursive) | `element.text` |
| `.get_text()` | Get all text | `element.get_text()` |
| `.attrs` | Get attributes dict | `element.attrs` |
| `['attribute']` | Get specific attribute | `element['href']` |

### Navigation

| Method | Description |
|--------|-------------|
| `.parent` | Get parent element |
| `.children` | Iterate through children |
| `.descendants` | Iterate through all descendants |
| `.next_sibling` | Next sibling element |
| `.previous_sibling` | Previous sibling element |

## CSS Selector Guide

Common CSS selectors work with BeautifulSoup:

```python
# Tag selector
soup.select('p')                    # All <p> tags

# Class selector
soup.select('.classname')           # All elements with class="classname"

# ID selector
soup.select('#id')                  # Element with id="id"

# Attribute selector
soup.select('[href]')               # All elements with href attribute

# Pseudo-selectors
soup.select('p:first-child')        # First child paragraphs
soup.select('div > p')              # Direct child paragraphs
soup.select('div p')                # All descendant paragraphs
```

## Web Scraping Ethics and Best Practices

### ✅ DO:
- Check website's `robots.txt` file
- Read and respect the website's Terms of Service
- Add delays between requests (use `time.sleep()`)
- Include a meaningful User-Agent header
- Only scrape data you have permission to access
- Store data responsibly
- Identify yourself in User-Agent when appropriate

### ❌ DON'T:
- Scrape sites that explicitly forbid it in robots.txt
- Overload servers with rapid requests
- Scrape personal or sensitive data
- Circumvent authentication or access controls
- Violate copyright or data protection laws
- Scrape data and claim it as your own

### Example: Respectful Scraping
```python
import requests
import time
from bs4 import BeautifulSoup

# Add identifying User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Educational Project)'
}

# Add delay between requests
for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Process data
    time.sleep(2)  # Wait 2 seconds between requests
```

## Real-World Project Ideas

1. **Movie Rankings Scraper**
   - Scrape Empire's 100 Greatest Movies
   - Extract title, rank, year, description
   - Store in JSON or CSV

2. **Price Comparison Tool**
   - Monitor product prices across sites
   - Alert on price drops
   - Track historical data

3. **Job Listing Aggregator**
   - Scrape job postings from multiple sites
   - Filter by location, salary, skills
   - Send email alerts for matches

4. **Weather Data Collection**
   - Scrape historical weather data
   - Analyze trends
   - Create visualizations

5. **Quote Extractor**
   - Scrape inspirational quotes
   - Categorize by author or topic
   - Build a random quote API

## Common Parsing Backends

BeautifulSoup supports multiple parsing engines:

| Parser | Pros | Cons |
|--------|------|------|
| `html.parser` | Built-in, no dependencies | Slower than alternatives |
| `lxml` | Fast and lenient | Requires additional installation |
| `html5lib` | Most lenient | Slow, requires additional installation |

```bash
# Install alternative parsers
pip install lxml html5lib
```

## Troubleshooting

### Issue: ImportError: No module named 'bs4'
```bash
pip install beautifulsoup4
```

### Issue: Website blocks scraping with 403 Forbidden
```python
# Add User-Agent header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(url, headers=headers)
```

### Issue: Finding elements returns None
- Verify the HTML structure using browser developer tools
- Check if the page loads with JavaScript (requests won't execute JS)
- Try different selectors or methods

### Issue: Slow parsing
```python
# Use lxml parser for better performance
soup = BeautifulSoup(html, 'lxml')
```

## Key Takeaways

1. **BeautifulSoup** makes parsing HTML intuitive and accessible
2. **Web scraping** is useful when APIs aren't available
3. **Respect robots.txt** and website terms of service
4. **Multiple methods** to find elements (find, find_all, select)
5. **CSS selectors** provide powerful and flexible element selection
6. **Ethical scraping** requires delays and proper headers
7. **Error handling** is essential for robust web scraping
8. **Static content** is easiest to scrape; JavaScript-rendered content requires additional tools

## Next Steps

1. Try scraping a simple website you own or have permission to scrape
2. Expand the examples to handle edge cases
3. Add error handling and logging
4. Store scraped data in a database (SQLite, PostgreSQL)
5. Learn about Scrapy for larger scraping projects
6. Explore Selenium for JavaScript-heavy websites

## Resources

- **BeautifulSoup Documentation**: https://www.crummy.com/software/BeautifulSoup/
- **Requests Library**: https://requests.readthedocs.io/
- **CSS Selectors Guide**: https://developer.mozilla.org/en-US/docs/Web/CSS/Selectors
- **Web Scraping Ethics**: https://www.scrapehero.com/web-scraping-best-practices/

---

**Date Created:** November 22, 2025  
**Project Type:** Web Scraping / Data Extraction  
**Difficulty Level:** Intermediate  
**Technologies:** Python, BeautifulSoup4, Requests, HTML, CSS Selectors
