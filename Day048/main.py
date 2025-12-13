"""
Day 48 - Selenium Web Automation & Browser Bot

Master browser automation using Selenium WebDriver to interact with websites
that require JavaScript execution or complex user interactions.

Project Goals:
1. Understand Selenium WebDriver architecture
2. Locate elements using multiple strategies
3. Interact with web elements (click, type, submit)
4. Handle dynamic content and waits
5. Navigate and manage browser windows
6. Execute JavaScript in the browser
7. Handle popup alerts and dialogs
8. Scrape JavaScript-rendered content

Selenium is essential for:
- Testing web applications
- Scraping JavaScript-heavy websites
- Automating repetitive tasks
- Interacting with SPAs (Single Page Applications)
- Bot automation with complex interactions

This project bridges the gap between static HTML scraping (BeautifulSoup)
and interactive web automation (Selenium).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# ============================================================================
# Configuration
# ============================================================================

# Chrome options for better performance and compatibility
CHROME_OPTIONS = [
    '--start-maximized',           # Start in maximized window
    '--disable-blink-features=AutomationControlled',  # Hide automation
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)',  # Realistic user agent
]

# Timeout for waiting for elements (in seconds)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 10

# ============================================================================
# WebDriver Management
# ============================================================================

def create_driver():
    """
    Create and configure a Chrome WebDriver instance.
    
    Returns:
        WebDriver: Configured Chrome driver
    """
    print("[CHROME] Creating Chrome WebDriver instance...")
    
    try:
        options = webdriver.ChromeOptions()
        
        # Add options
        for option in CHROME_OPTIONS:
            options.add_argument(option)
        
        # Additional useful options
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        options.add_argument('--no-sandbox')   # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        
        print("[OK] WebDriver created successfully!\n")
        return driver
        
    except Exception as e:
        print(f"[ERROR] Failed to create WebDriver: {e}")
        print("[INFO] Make sure ChromeDriver is installed and in PATH")
        print("[INFO] Download from: https://chromedriver.chromium.org/\n")
        return None


def close_driver(driver):
    """
    Close the WebDriver and clean up resources.
    
    Args:
        driver: WebDriver instance to close
    """
    if driver:
        try:
            driver.quit()
            print("[OK] WebDriver closed successfully.\n")
        except Exception as e:
            print(f"[WARNING] Error closing driver: {e}\n")


# ============================================================================
# Element Location Strategies
# ============================================================================

def find_element_by_id(driver, element_id, wait_time=EXPLICIT_WAIT):
    """
    Find element by ID attribute.
    
    Args:
        driver: WebDriver instance
        element_id: ID of element
        wait_time: Timeout in seconds
    
    Returns:
        WebElement or None
    """
    try:
        print(f"[FIND] Searching for element with ID: {element_id}")
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        print(f"[OK] Element found!\n")
        return element
    except Exception as e:
        print(f"[ERROR] Element not found: {e}\n")
        return None


def find_element_by_xpath(driver, xpath, wait_time=EXPLICIT_WAIT):
    """
    Find element by XPath expression.
    
    Args:
        driver: WebDriver instance
        xpath: XPath expression
        wait_time: Timeout in seconds
    
    Returns:
        WebElement or None
    """
    try:
        print(f"[FIND] Searching for element with XPath: {xpath}")
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(f"[OK] Element found!\n")
        return element
    except Exception as e:
        print(f"[ERROR] Element not found: {e}\n")
        return None


def find_element_by_css(driver, css_selector, wait_time=EXPLICIT_WAIT):
    """
    Find element by CSS selector.
    
    Args:
        driver: WebDriver instance
        css_selector: CSS selector string
        wait_time: Timeout in seconds
    
    Returns:
        WebElement or None
    """
    try:
        print(f"[FIND] Searching for element with CSS: {css_selector}")
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        print(f"[OK] Element found!\n")
        return element
    except Exception as e:
        print(f"[ERROR] Element not found: {e}\n")
        return None


def find_elements(driver, locator_type, locator_value):
    """
    Find multiple elements.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.CSS_SELECTOR, By.XPATH, etc.
        locator_value: Locator value
    
    Returns:
        List of WebElements
    """
    try:
        elements = driver.find_elements(locator_type, locator_value)
        print(f"[OK] Found {len(elements)} elements\n")
        return elements
    except Exception as e:
        print(f"[ERROR] Failed to find elements: {e}\n")
        return []


# ============================================================================
# Element Interaction
# ============================================================================

def click_element(driver, element):
    """
    Click an element.
    
    Args:
        driver: WebDriver instance
        element: WebElement to click
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        
        # Click element
        element.click()
        print("[OK] Element clicked successfully!\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to click element: {e}\n")
        return False


def type_text(driver, element, text):
    """
    Type text into an input field.
    
    Args:
        driver: WebDriver instance
        element: Input WebElement
        text: Text to type
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Clear existing text
        element.clear()
        
        # Type new text
        element.send_keys(text)
        print(f"[OK] Typed '{text}' into element\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to type text: {e}\n")
        return False


def submit_form(driver, element):
    """
    Submit a form element.
    
    Args:
        driver: WebDriver instance
        element: Form WebElement
    
    Returns:
        True if successful, False otherwise
    """
    try:
        element.submit()
        print("[OK] Form submitted successfully!\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to submit form: {e}\n")
        return False


def get_element_text(element):
    """
    Get text content of an element.
    
    Args:
        element: WebElement
    
    Returns:
        Text content or None
    """
    try:
        text = element.text
        print(f"[TEXT] '{text}'\n")
        return text
    except Exception as e:
        print(f"[ERROR] Failed to get text: {e}\n")
        return None


def get_element_attribute(element, attribute_name):
    """
    Get an attribute value from an element.
    
    Args:
        element: WebElement
        attribute_name: Attribute to retrieve
    
    Returns:
        Attribute value or None
    """
    try:
        value = element.get_attribute(attribute_name)
        print(f"[ATTR] {attribute_name} = {value}\n")
        return value
    except Exception as e:
        print(f"[ERROR] Failed to get attribute: {e}\n")
        return None


# ============================================================================
# Navigation & Page Management
# ============================================================================

def navigate_to(driver, url):
    """
    Navigate to a URL.
    
    Args:
        driver: WebDriver instance
        url: URL to navigate to
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[NAV] Navigating to: {url}")
        driver.get(url)
        print("[OK] Page loaded!\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to navigate: {e}\n")
        return False


def go_back(driver):
    """
    Go back to previous page.
    
    Args:
        driver: WebDriver instance
    """
    try:
        driver.back()
        print("[OK] Navigated back\n")
    except Exception as e:
        print(f"[ERROR] Failed to go back: {e}\n")


def go_forward(driver):
    """
    Go forward to next page.
    
    Args:
        driver: WebDriver instance
    """
    try:
        driver.forward()
        print("[OK] Navigated forward\n")
    except Exception as e:
        print(f"[ERROR] Failed to go forward: {e}\n")


def refresh_page(driver):
    """
    Refresh the current page.
    
    Args:
        driver: WebDriver instance
    """
    try:
        driver.refresh()
        print("[OK] Page refreshed\n")
    except Exception as e:
        print(f"[ERROR] Failed to refresh: {e}\n")


def get_page_title(driver):
    """
    Get the page title.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        Page title or None
    """
    try:
        title = driver.title
        print(f"[TITLE] {title}\n")
        return title
    except Exception as e:
        print(f"[ERROR] Failed to get title: {e}\n")
        return None


def get_page_source(driver):
    """
    Get the page source HTML.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        HTML source or None
    """
    try:
        source = driver.page_source
        print(f"[SOURCE] Retrieved {len(source)} characters\n")
        return source
    except Exception as e:
        print(f"[ERROR] Failed to get source: {e}\n")
        return None


# ============================================================================
# Waiting Strategies
# ============================================================================

def wait_for_element_visibility(driver, locator_type, locator_value, timeout=EXPLICIT_WAIT):
    """
    Wait for an element to become visible.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.CSS_SELECTOR, etc.
        locator_value: Locator value
        timeout: Maximum wait time
    
    Returns:
        WebElement or None
    """
    try:
        print("[WAIT] Waiting for element to be visible...")
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((locator_type, locator_value))
        )
        print("[OK] Element is visible!\n")
        return element
    except Exception as e:
        print(f"[ERROR] Element did not become visible: {e}\n")
        return None


def wait_for_element_clickable(driver, locator_type, locator_value, timeout=EXPLICIT_WAIT):
    """
    Wait for an element to become clickable.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.CSS_SELECTOR, etc.
        locator_value: Locator value
        timeout: Maximum wait time
    
    Returns:
        WebElement or None
    """
    try:
        print("[WAIT] Waiting for element to be clickable...")
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        print("[OK] Element is clickable!\n")
        return element
    except Exception as e:
        print(f"[ERROR] Element is not clickable: {e}\n")
        return None


def wait_for_text(driver, locator_type, locator_value, text, timeout=EXPLICIT_WAIT):
    """
    Wait for an element to contain specific text.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.CSS_SELECTOR, etc.
        locator_value: Locator value
        text: Text to wait for
        timeout: Maximum wait time
    
    Returns:
        WebElement or None
    """
    try:
        print(f"[WAIT] Waiting for element to contain: '{text}'")
        element = WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element((locator_type, locator_value), text)
        )
        print("[OK] Text found!\n")
        return driver.find_element(locator_type, locator_value)
    except Exception as e:
        print(f"[ERROR] Text not found: {e}\n")
        return None


# ============================================================================
# JavaScript Execution
# ============================================================================

def execute_javascript(driver, script, *args):
    """
    Execute JavaScript in the browser context.
    
    Args:
        driver: WebDriver instance
        script: JavaScript code to execute
        *args: Arguments to pass to the script
    
    Returns:
        Result of JavaScript execution or None
    """
    try:
        result = driver.execute_script(script, *args)
        print(f"[JS] Executed: {script[:50]}...")
        if result:
            print(f"[RESULT] {result}\n")
        return result
    except Exception as e:
        print(f"[ERROR] Failed to execute JavaScript: {e}\n")
        return None


def scroll_to_bottom(driver):
    """
    Scroll to the bottom of the page.
    
    Args:
        driver: WebDriver instance
    """
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("[OK] Scrolled to bottom\n")
    except Exception as e:
        print(f"[ERROR] Failed to scroll: {e}\n")


def scroll_to_element(driver, element):
    """
    Scroll to a specific element.
    
    Args:
        driver: WebDriver instance
        element: WebElement to scroll to
    """
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print("[OK] Scrolled to element\n")
    except Exception as e:
        print(f"[ERROR] Failed to scroll to element: {e}\n")


# ============================================================================
# Window & Alert Handling
# ============================================================================

def get_window_handle(driver):
    """
    Get the current window handle.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        Window handle string
    """
    try:
        handle = driver.current_window_handle
        print(f"[WINDOW] Current handle: {handle}\n")
        return handle
    except Exception as e:
        print(f"[ERROR] Failed to get window handle: {e}\n")
        return None


def switch_to_window(driver, window_handle):
    """
    Switch to a specific window.
    
    Args:
        driver: WebDriver instance
        window_handle: Handle of window to switch to
    """
    try:
        driver.switch_to.window(window_handle)
        print("[OK] Switched to window\n")
    except Exception as e:
        print(f"[ERROR] Failed to switch window: {e}\n")


def switch_to_iframe(driver, iframe_locator):
    """
    Switch to an iframe.
    
    Args:
        driver: WebDriver instance
        iframe_locator: Locator for iframe element
    """
    try:
        driver.switch_to.frame(iframe_locator)
        print("[OK] Switched to iframe\n")
    except Exception as e:
        print(f"[ERROR] Failed to switch to iframe: {e}\n")


def switch_to_default_content(driver):
    """
    Switch back to main content from iframe.
    
    Args:
        driver: WebDriver instance
    """
    try:
        driver.switch_to.default_content()
        print("[OK] Switched to default content\n")
    except Exception as e:
        print(f"[ERROR] Failed to switch content: {e}\n")


def handle_alert(driver, accept=True):
    """
    Handle JavaScript alert dialogs.
    
    Args:
        driver: WebDriver instance
        accept: True to accept, False to dismiss
    
    Returns:
        Alert text or None
    """
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"[ALERT] {alert_text}")
        
        if accept:
            alert.accept()
            print("[OK] Alert accepted\n")
        else:
            alert.dismiss()
            print("[OK] Alert dismissed\n")
        
        return alert_text
    except Exception as e:
        print(f"[ERROR] Failed to handle alert: {e}\n")
        return None


# ============================================================================
# Demonstration & Examples
# ============================================================================

def demonstrate_selenium():
    """
    Demonstrate key Selenium features and best practices.
    """
    print()
    print("=" * 70)
    print("Selenium Web Automation - Demonstration".center(70))
    print("=" * 70)
    print()
    
    print("[INFO] This script demonstrates Selenium WebDriver capabilities.\n")
    
    # Create driver
    driver = create_driver()
    
    if not driver:
        print("[ERROR] Could not create WebDriver. Exiting.")
        return
    
    try:
        # Example 1: Basic Navigation
        print("=" * 70)
        print("Example 1: Basic Navigation & Page Inspection".center(70))
        print("=" * 70)
        print()
        
        navigate_to(driver, "https://www.python.org")
        time.sleep(2)
        
        title = get_page_title(driver)
        print(f"Page title: {title}\n")
        
        # Example 2: Element Interaction
        print("=" * 70)
        print("Example 2: Finding & Interacting with Elements".center(70))
        print("=" * 70)
        print()
        
        # Find search box
        search_box = find_element_by_name(driver, "q")
        if search_box:
            type_text(driver, search_box, "Django")
            time.sleep(1)
        
        print()
        
        # Example 3: Page Source
        print("=" * 70)
        print("Example 3: Accessing Page Source".center(70))
        print("=" * 70)
        print()
        
        source = get_page_source(driver)
        if source:
            print(f"Page source length: {len(source)} characters\n")
        
        # Example 4: JavaScript Execution
        print("=" * 70)
        print("Example 4: Executing JavaScript".center(70))
        print("=" * 70)
        print()
        
        title_via_js = execute_javascript(driver, "return document.title;")
        print(f"Title via JavaScript: {title_via_js}\n")
        
        # Example 5: Scrolling
        print("=" * 70)
        print("Example 5: Scrolling Operations".center(70))
        print("=" * 70)
        print()
        
        scroll_to_bottom(driver)
        time.sleep(1)
        
        print()
        
    finally:
        close_driver(driver)
    
    print("=" * 70)
    print("Demonstration Complete!".center(70))
    print("=" * 70)
    print()


def find_element_by_name(driver, name, wait_time=EXPLICIT_WAIT):
    """
    Find element by name attribute.
    
    Args:
        driver: WebDriver instance
        name: Name attribute value
        wait_time: Timeout in seconds
    
    Returns:
        WebElement or None
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.NAME, name))
        )
        return element
    except:
        return None


def display_key_concepts():
    """
    Display key Selenium concepts and best practices.
    """
    print()
    print("=" * 70)
    print("Key Selenium Concepts & Best Practices".center(70))
    print("=" * 70)
    print("""
1. LOCATING ELEMENTS
   - By.ID: Most reliable if ID is unique
   - By.CSS_SELECTOR: Fast and flexible
   - By.XPATH: Most powerful but slower
   - By.CLASS_NAME: Good for multiple matches
   - By.NAME: Good for form elements
   - By.LINK_TEXT: For links

2. WAITING STRATEGIES
   - Implicit Wait: Applied to all find operations
   - Explicit Wait: Applied to specific operations
   - WebDriverWait + Expected Conditions
   - Best Practice: Use explicit waits for dynamic content

3. ELEMENT INTERACTIONS
   - click(): Click element
   - send_keys(): Type text
   - clear(): Clear input field
   - submit(): Submit form
   - get_attribute(): Read attributes
   - text: Read visible text

4. NAVIGATION
   - driver.get(url): Load a URL
   - driver.back(): Go back
   - driver.forward(): Go forward
   - driver.refresh(): Refresh page

5. JAVASCRIPT EXECUTION
   - execute_script(): Run JavaScript
   - Useful for: Scrolling, clicking hidden elements, getting computed styles
   - Always sanitize user input

6. WINDOW & FRAME HANDLING
   - switch_to.window(): Switch between windows
   - switch_to.frame(): Switch to iframe
   - switch_to.alert(): Handle alerts
   - switch_to.default_content(): Exit iframe

7. BEST PRACTICES
   - Use explicit waits, not time.sleep()
   - Set implicit wait once, not repeatedly
   - Always clean up: driver.quit()
   - Use try/finally for cleanup
   - Scroll elements into view before clicking
   - Handle exceptions gracefully
   - Use realistic User-Agent headers
   - Respect website rate limits
   - Check robots.txt and Terms of Service

8. COMMON CHALLENGES
   - StaleElementReferenceException: Element is no longer valid
   - NoSuchElementException: Element not found
   - TimeoutException: Element not found within timeout
   - Solution: Use explicit waits, not implicit waits alone

9. PERFORMANCE TIPS
   - Headless mode for speed: --headless
   - Disable images: --blink-features=AutomationControlled
   - Use specific waits, not general sleep()
   - Close unnecessary tabs/windows
   - Use WebDriverWait for reliability

10. SELENIUM VS BEAUTIFULSOUP
    - BeautifulSoup: Fast, static HTML only
    - Selenium: Slower, handles JavaScript, interactive
    - Hybrid approach: Selenium + BeautifulSoup for best results
    """)


def main():
    """
    Main program entry point.
    """
    print()
    print("=" * 70)
    print("Day 48 - Selenium Web Automation & Browser Bot".center(70))
    print("=" * 70)
    print()
    
    print("Learn to automate web browsers using Selenium WebDriver.\n")
    
    print("Key Features:")
    print("  - Create and manage Chrome WebDriver")
    print("  - Find elements using multiple strategies")
    print("  - Interact with web elements")
    print("  - Handle dynamic content with waits")
    print("  - Execute JavaScript in browser")
    print("  - Manage windows and iframes")
    print("  - Handle alerts and popups\n")
    
    display_key_concepts()
    
    print("=" * 70)
    print("Getting Started".center(70))
    print("=" * 70)
    print("""
1. INSTALLATION
   pip install selenium

2. DOWNLOAD CHROMEDRIVER
   - Visit: https://chromedriver.chromium.org/
   - Download version matching your Chrome browser
   - Extract and add to PATH or specify in code

3. BASIC USAGE
   driver = create_driver()
   navigate_to(driver, "https://example.com")
   element = find_element_by_id(driver, "element-id")
   click_element(driver, element)
   close_driver(driver)

4. RUNNING DEMONSTRATIONS
   - Uncomment: demonstrate_selenium()
   - Or write your own automation scripts

5. BEST PRACTICES
   - Always use explicit waits for dynamic content
   - Close driver in finally block
   - Use headless mode for background tasks
   - Handle exceptions at every step
   - Respect website rate limits

""")
    
    print("=" * 70)
    print("[INFO] Ready to automate web interactions with Selenium!".center(70))
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
    
    # Uncomment to run demonstration (requires internet)
    # demonstrate_selenium()