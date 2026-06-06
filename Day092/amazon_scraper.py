from bs4 import BeautifulSoup
import csv
import os
import re

SAMPLE_HTML = os.path.join(os.path.dirname(__file__), "sample_products.html")


def parse_amazon_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    products = []
    cards = soup.select("div[data-component-type='s-search-result']")

    for card in cards:
        title_elem = card.select_one("h2 a span")
        price_whole = card.select_one(".a-price-whole")
        price_fraction = card.select_one(".a-price-fraction")
        rating_elem = card.select_one(".a-icon-alt")
        reviews_elem = card.select_one(".a-size-base.s-underline-text")

        title = title_elem.text.strip() if title_elem else "N/A"
        price = None
        if price_whole:
            price = price_whole.text.strip().replace(",", "")
            if price_fraction:
                price += "." + price_fraction.text.strip()
            price = float(price)
        rating = None
        if rating_elem:
            match = re.search(r"([\d.]+)", rating_elem.text)
            if match:
                rating = float(match.group(1))
        reviews = None
        if reviews_elem:
            reviews_text = reviews_elem.text.strip().replace(",", "")
            reviews = int(reviews_text) if reviews_text.isdigit() else None

        availability = "In Stock"
        if card.select_one(".a-color-price"):
            availability = "Available"
        if card.select_one(".a-color-error"):
            availability = "Currently Unavailable"

        products.append({
            "title": title,
            "price_usd": price,
            "rating": rating,
            "reviews": reviews,
            "availability": availability,
        })

    return products


def main():
    print("=" * 50)
    print("AMAZON PRODUCT SCRAPER")
    print("=" * 50)

    if not os.path.exists(SAMPLE_HTML):
        print(f"Sample HTML not found: {SAMPLE_HTML}")
        print("Create a sample_products.html file with Amazon search result HTML to test.")
        return

    print(f"Parsing: {SAMPLE_HTML}")
    products = parse_amazon_html(SAMPLE_HTML)

    print(f"\nFound {len(products)} products:\n")
    for i, product in enumerate(products, 1):
        price_str = f"${product['price_usd']:.2f}" if product["price_usd"] else "N/A"
        rating_str = f"{product['rating']}★" if product["rating"] else "N/A"
        reviews_str = f"({product['reviews']})" if product["reviews"] else ""
        print(f"{i}. {product['title'][:80]}...")
        print(f"   Price: {price_str} | Rating: {rating_str} {reviews_str} | {product['availability']}")

    output_csv = os.path.join(os.path.dirname(__file__), "products.csv")
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price_usd", "rating", "reviews", "availability"])
        writer.writeheader()
        writer.writerows(products)

    print(f"\nData saved to: {output_csv}")


if __name__ == "__main__":
    main()
