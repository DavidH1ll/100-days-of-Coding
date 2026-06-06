"""News fetching module using NewsAPI.

Retrieves recent news articles about a company or topic.
"""
from __future__ import annotations

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional


NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_news(
    query: str,
    api_key: str,
    days_back: int = 7,
    language: str = "en",
    sort_by: str = "publishedAt"
) -> Optional[List[Dict[str, str]]]:
    """Fetch recent news articles matching a query.
    
    Args:
        query: Search term (e.g., company name)
        api_key: NewsAPI key
        days_back: How many days back to search
        language: Article language
        sort_by: Sort order (publishedAt, relevancy, popularity)
    
    Returns:
        List of article dicts with keys: title, description, url, publishedAt, source
    """
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    params = {
        "q": query,
        "from": from_date,
        "language": language,
        "sortBy": sort_by,
        "apiKey": api_key
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            print(f"[ERROR] NewsAPI: {data.get('message', 'Unknown error')}")
            return None
        
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description"),
                "url": article.get("url", ""),
                "publishedAt": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", "Unknown")
            })
        
        return articles
    
    except requests.RequestException as e:
        print(f"[ERROR] News API request failed: {e}")
        return None


def format_articles(articles: List[Dict[str, str]], max_count: int = 3) -> str:
    """Format news articles into a readable string.
    
    Args:
        articles: List of article dicts
        max_count: Maximum number of articles to include
    
    Returns:
        Formatted string with article headlines and links
    """
    if not articles:
        return "No recent news found."
    
    lines = []
    for i, article in enumerate(articles[:max_count], 1):
        title = article["title"]
        source = article["source"]
        url = article["url"]
        lines.append(f"{i}. {title}")
        lines.append(f"   Source: {source}")
        lines.append(f"   {url}\n")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test
    api_key = os.getenv("NEWS_API_KEY")
    company = os.getenv("COMPANY_NAME", "Tesla")
    
    if api_key:
        articles = fetch_news(company, api_key, days_back=3)
        if articles:
            print(f"Found {len(articles)} articles about {company}:\n")
            print(format_articles(articles, max_count=3))
    else:
        print("Set NEWS_API_KEY to test")
