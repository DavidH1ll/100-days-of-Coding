from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===========================
# PART 1: WEB SCRAPING WITH BEAUTIFUL SOUP
# ===========================

# URL of the Zillow Clone website
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone"

# Scrape the website
response = requests.get(ZILLOW_CLONE_URL)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

# Extract all listings
listings = soup.find_all("div", class_="listing")

# Lists to store scraped data
prices = []
addresses = []
links = []

# Parse each listing
for listing in listings:
    # Extract price
    try:
        price_text = listing.find("span", class_="listing-price").get_text(strip=True)
        # Clean price: remove "+", "/mo", and extra whitespace
        cleaned_price = price_text.replace("+", "").replace("/mo", "").strip()
        prices.append(cleaned_price)
    except (AttributeError, TypeError):
        prices.append("N/A")
    
    # Extract address
    try:
        address_text = listing.find("a", class_="listing-heading").get_text(strip=True)
        # Clean address: remove newlines, pipes, and extra whitespace
        cleaned_address = " ".join(address_text.split())
        cleaned_address = cleaned_address.replace("|", "").strip()
        addresses.append(cleaned_address)
    except (AttributeError, TypeError):
        addresses.append("N/A")
    
    # Extract link
    try:
        link = listing.find("a", class_="listing-heading")["href"]
        # Convert relative URLs to absolute URLs if needed
        if link.startswith("http"):
            links.append(link)
        else:
            links.append(ZILLOW_CLONE_URL + link)
    except (AttributeError, TypeError, KeyError):
        links.append("N/A")

print(f"Scraped {len(listings)} listings")
print(f"Prices: {prices}")
print(f"Addresses: {addresses}")
print(f"Links: {links}")

# ===========================
# PART 2: FILL GOOGLE FORM WITH SELENIUM
# ===========================

# Replace this with your own Google Form URL
GOOGLE_FORM_URL = "YOUR_GOOGLE_FORM_URL_HERE"

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Fill out the form for each listing
    for i in range(len(listings)):
        # Navigate to the form
        driver.get(GOOGLE_FORM_URL)
        
        # Wait for the page to load
        time.sleep(2)
        
        # Find all text input fields
        # Typically, Google Forms has input fields in order: address, price, link
        input_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
        
        # Wait for inputs to be visible
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[type='text'], textarea")))
        
        # Fill in the form fields
        if len(input_fields) >= 3:
            # First field: Address
            input_fields[0].click()
            input_fields[0].send_keys(addresses[i])
            
            # Second field: Price
            input_fields[1].click()
            input_fields[1].send_keys(prices[i])
            
            # Third field: Link
            input_fields[2].click()
            input_fields[2].send_keys(links[i])
        
        # Find and click the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit'], button[type='submit']")
        submit_button.click()
        
        print(f"Submitted form {i + 1}: {addresses[i]} - {prices[i]}")
        
        # Wait a moment between submissions
        time.sleep(1)

finally:
    # Close the browser
    driver.quit()

print("All forms submitted successfully!")
