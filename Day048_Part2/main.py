"""
Day 49 - Form Automation and Element Interaction with Selenium 

Master the art of interacting with web elements programmatically.
This lesson focuses on practical techniques for form filling, button clicking,
and keyboard interactions that simulate real user behavior.

Project Goals:
1. Click buttons and links programmatically
2. Type text into input fields
3. Send special keyboard keys (ENTER, TAB, etc.)
4. Interact with form elements (select, radio, checkbox)
5. Handle form submission and validation
6. Simulate complex user workflows
7. Automate repetitive web tasks
8. Handle dynamic element interactions

Key Skills:
- Element.click() for button/link interaction
- Element.send_keys() for text input
- Keys class for special keyboard actions
- Form finding and interaction patterns
- Workflow automation chains
- Error handling for interactive elements

Real-World Applications:
- Automated form submission bots
- Web testing automation
- Data entry automation
- Account creation workflows
- Search and filter automation
- Multi-step process automation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# ============================================================================
# Configuration
# ============================================================================

# Test websites for form automation practice
TEST_SITES = {
    'form_site': 'https://practice-automation.com/',
    'sign_up_form': 'https://practice-automation.com/form-submission/',
    'checkbox_form': 'https://practice-automation.com/checkboxes/',
    'dropdown': 'https://practice-automation.com/dropdown/',
    'input_fields': 'https://practice-automation.com/text-inputs/',
}

# Timeout for waits
TIMEOUT = 10

# ============================================================================
# Basic Element Interaction
# ============================================================================

def click_element(driver, locator_type, locator_value):
    """
    Find and click an element.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.CLASS_NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[CLICK] Finding element with {locator_type}: {locator_value}")
        
        # Wait for element to be clickable
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)
        
        # Click
        element.click()
        print("[OK] Element clicked successfully!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to click element: {e}\n")
        return False


def click_link_by_text(driver, link_text):
    """
    Find and click a link by its text content.
    
    Args:
        driver: WebDriver instance
        link_text: Exact text of the link
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[CLICK] Finding link with text: '{link_text}'")
        
        link = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        
        link.click()
        print("[OK] Link clicked successfully!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to click link: {e}\n")
        return False


def click_partial_link_text(driver, partial_text):
    """
    Find and click a link by partial text match.
    
    Args:
        driver: WebDriver instance
        partial_text: Partial text of the link
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[CLICK] Finding link with partial text: '{partial_text}'")
        
        link = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, partial_text))
        )
        
        link.click()
        print("[OK] Link clicked successfully!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to click link: {e}\n")
        return False


# ============================================================================
# Text Input Interaction
# ============================================================================

def type_into_field(driver, locator_type, locator_value, text, clear_first=True):
    """
    Find an input field and type text into it.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
        text: Text to type
        clear_first: Whether to clear field before typing
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[TYPE] Finding input field with {locator_type}: {locator_value}")
        
        # Find input element
        input_element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((locator_type, locator_value))
        )
        
        # Clear field if requested
        if clear_first:
            input_element.clear()
            print("[OK] Field cleared")
        
        # Type text
        input_element.send_keys(text)
        print(f"[OK] Typed: '{text}'\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to type into field: {e}\n")
        return False


def type_into_field_by_name(driver, field_name, text, clear_first=True):
    """
    Find and type into input field by name attribute.
    
    Args:
        driver: WebDriver instance
        field_name: Name attribute value
        text: Text to type
        clear_first: Whether to clear field first
    
    Returns:
        True if successful, False otherwise
    """
    return type_into_field(driver, By.NAME, field_name, text, clear_first)


def type_into_field_by_id(driver, element_id, text, clear_first=True):
    """
    Find and type into input field by ID.
    
    Args:
        driver: WebDriver instance
        element_id: Element ID
        text: Text to type
        clear_first: Whether to clear field first
    
    Returns:
        True if successful, False otherwise
    """
    return type_into_field(driver, By.ID, element_id, text, clear_first)


def clear_input_field(driver, locator_type, locator_value):
    """
    Clear an input field.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[CLEAR] Finding field with {locator_type}: {locator_value}")
        
        field = driver.find_element(locator_type, locator_value)
        
        # Clear using Ctrl+A then Delete
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        
        print("[OK] Field cleared!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to clear field: {e}\n")
        return False


# ============================================================================
# Special Keys and Keyboard Interaction
# ============================================================================

def send_special_key(driver, locator_type, locator_value, key):
    """
    Send a special key to an element.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
        key: Key to send (Keys.ENTER, Keys.TAB, etc.)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[KEY] Sending special key to element")
        
        element = driver.find_element(locator_type, locator_value)
        element.send_keys(key)
        
        print("[OK] Key sent successfully!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send key: {e}\n")
        return False


def press_enter(driver, locator_type, locator_value):
    """
    Press ENTER key on an element.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    return send_special_key(driver, locator_type, locator_value, Keys.ENTER)


def press_tab(driver, locator_type, locator_value):
    """
    Press TAB key on an element.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    return send_special_key(driver, locator_type, locator_value, Keys.TAB)


def press_escape(driver):
    """
    Press ESCAPE key globally.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("[KEY] Pressing ESCAPE")
        
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        
        print("[OK] ESCAPE pressed!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to press ESCAPE: {e}\n")
        return False


def send_keyboard_shortcut(driver, *keys):
    """
    Send keyboard shortcut combination (e.g., Ctrl+C).
    
    Args:
        driver: WebDriver instance
        *keys: Keys to press (Keys.CONTROL, "c", etc.)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("[KEY] Sending keyboard shortcut")
        
        body = driver.find_element(By.TAG_NAME, "body")
        combination = "".join(keys)
        body.send_keys(combination)
        
        print("[OK] Shortcut sent!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send shortcut: {e}\n")
        return False


# ============================================================================
# Form Interaction
# ============================================================================

def submit_form(driver, locator_type, locator_value):
    """
    Submit a form element.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.CSS_SELECTOR, etc.
        locator_value: Value to locate form
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[FORM] Finding form element")
        
        form = driver.find_element(locator_type, locator_value)
        form.submit()
        
        print("[OK] Form submitted!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to submit form: {e}\n")
        return False


def find_form_button(driver, form_selector, button_text=None):
    """
    Find a button within a form.
    
    Args:
        driver: WebDriver instance
        form_selector: CSS selector or XPath for form
        button_text: Optional button text to find specific button
    
    Returns:
        WebElement or None
    """
    try:
        print("[FORM] Finding button in form")
        
        if button_text:
            # Find button with specific text
            button = driver.find_element(
                By.XPATH,
                f"{form_selector}//button[contains(text(), '{button_text}')]"
            )
        else:
            # Find first button
            button = driver.find_element(By.CSS_SELECTOR, f"{form_selector} button")
        
        print("[OK] Button found!\n")
        return button
        
    except Exception as e:
        print(f"[ERROR] Failed to find button: {e}\n")
        return None


def fill_form_field(driver, field_name, value):
    """
    Fill a form field by name attribute.
    
    Args:
        driver: WebDriver instance
        field_name: Name attribute value
        value: Value to enter
    
    Returns:
        True if successful, False otherwise
    """
    return type_into_field_by_name(driver, field_name, value)


def select_checkbox(driver, locator_type, locator_value):
    """
    Select a checkbox if not already selected.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[CHECK] Finding checkbox")
        
        checkbox = driver.find_element(locator_type, locator_value)
        
        if not checkbox.is_selected():
            checkbox.click()
            print("[OK] Checkbox selected!\n")
        else:
            print("[INFO] Checkbox already selected\n")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to select checkbox: {e}\n")
        return False


def unselect_checkbox(driver, locator_type, locator_value):
    """
    Unselect a checkbox if selected.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[UNCHECK] Finding checkbox")
        
        checkbox = driver.find_element(locator_type, locator_value)
        
        if checkbox.is_selected():
            checkbox.click()
            print("[OK] Checkbox unselected!\n")
        else:
            print("[INFO] Checkbox already unselected\n")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to unselect checkbox: {e}\n")
        return False


def select_radio_button(driver, locator_type, locator_value):
    """
    Select a radio button.
    
    Args:
        driver: WebDriver instance
        locator_type: By.ID, By.NAME, etc.
        locator_value: Value to locate
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[RADIO] Finding radio button")
        
        radio = driver.find_element(locator_type, locator_value)
        
        if not radio.is_selected():
            radio.click()
            print("[OK] Radio button selected!\n")
        else:
            print("[INFO] Radio button already selected\n")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to select radio button: {e}\n")
        return False


def select_dropdown_option(driver, dropdown_selector, option_value):
    """
    Select an option from a dropdown by value.
    
    Args:
        driver: WebDriver instance
        dropdown_selector: Selector for dropdown element
        option_value: Value of option to select
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[DROPDOWN] Finding dropdown element")
        
        from selenium.webdriver.support.select import Select
        
        dropdown = driver.find_element(By.CSS_SELECTOR, dropdown_selector)
        select = Select(dropdown)
        select.select_by_value(option_value)
        
        print(f"[OK] Option selected!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to select option: {e}\n")
        return False


# ============================================================================
# Complex Workflows
# ============================================================================

def fill_signup_form(driver, first_name, last_name, email):
    """
    Fill a typical signup form with three fields and submit.
    
    Args:
        driver: WebDriver instance
        first_name: First name value
        last_name: Last name value
        email: Email value
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("=" * 70)
        print("Filling Signup Form".center(70))
        print("=" * 70)
        print()
        
        # Fill first name
        if not fill_form_field(driver, "fName", first_name):
            return False
        
        # Fill last name
        if not fill_form_field(driver, "lName", last_name):
            return False
        
        # Fill email
        if not fill_form_field(driver, "email", email):
            return False
        
        # Click submit button
        print("[FORM] Clicking submit button")
        button = driver.find_element(By.CSS_SELECTOR, "form button")
        button.click()
        
        print("[OK] Form submitted!\n")
        
        # Wait for success
        time.sleep(2)
        
        print("=" * 70)
        print("Form submission complete!".center(70))
        print("=" * 70)
        print()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to fill form: {e}\n")
        return False


def search_and_filter_workflow(driver, search_term, filter_option=None):
    """
    Complete a search and optional filter workflow.
    
    Args:
        driver: WebDriver instance
        search_term: Term to search for
        filter_option: Optional filter to apply
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("=" * 70)
        print("Search and Filter Workflow".center(70))
        print("=" * 70)
        print()
        
        # Find search input
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys(search_term)
        print(f"[OK] Typed search term: {search_term}\n")
        
        # Press Enter to search
        search_box.send_keys(Keys.ENTER)
        print("[OK] Search submitted\n")
        
        # Wait for results
        time.sleep(2)
        
        # Apply filter if provided
        if filter_option:
            filter_elem = driver.find_element(By.ID, "filter")
            filter_elem.click()
            print(f"[OK] Applied filter: {filter_option}\n")
            time.sleep(1)
        
        print("=" * 70)
        print("Search workflow complete!".center(70))
        print("=" * 70)
        print()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Workflow failed: {e}\n")
        return False


# ============================================================================
# Best Practices & Demonstration
# ============================================================================

def display_interaction_tips():
    """
    Display best practices for form and element interaction.
    """
    print()
    print("=" * 70)
    print("Form & Element Interaction Best Practices".center(70))
    print("=" * 70)
    print("""
1. CLICKING ELEMENTS
   - Always wait for element to be clickable (not just visible)
   - Scroll element into view before clicking
   - Use try/except for error handling
   - Some elements may require JavaScript click: execute_script("arguments[0].click();", element)

2. TYPING INTO FIELDS
   - Clear field first using .clear() or Ctrl+A + Delete
   - Use send_keys() for normal text
   - Check field is enabled/editable before typing
   - Handle "placeholder" text differently than actual values

3. SPECIAL KEYS
   - Keys.ENTER: Submit forms or confirm actions
   - Keys.TAB: Move to next field
   - Keys.ESCAPE: Close modals/popups
   - Keys.DELETE: Clear text
   - Keys.BACKSPACE: Delete previous character
   - Keys.CONTROL: Combine with other keys (Ctrl+A, Ctrl+C)

4. FINDING ELEMENTS EFFECTIVELY
   - By.NAME: For form fields (input type="text" name="field")
   - By.ID: For unique elements (fastest)
   - By.CSS_SELECTOR: For complex selections
   - By.XPATH: For most flexible searching
   - By.LINK_TEXT: For exact link matching
   - By.PARTIAL_LINK_TEXT: For partial link matching

5. FORM SUBMISSION
   - Method 1: Click submit button
   - Method 2: Call form.submit() directly
   - Method 3: Press ENTER from last field
   - Wait for page change after submission

6. HANDLING FORM VALIDATION
   - Check for error messages after submission
   - Verify success message appears
   - Confirm URL change or page redirect
   - Wait for expected success conditions

7. DROPDOWN SELECTION
   - Use Select class from selenium.webdriver.support.select
   - select_by_value(): Select by value attribute
   - select_by_text(): Select by visible text
   - select_by_index(): Select by position

8. CHECKBOX AND RADIO HANDLING
   - Use .is_selected() to check current state
   - Click to toggle state
   - Can use .click() or driver.execute_script()
   - Verify state after clicking

9. ERROR HANDLING
   - Element not found: Use explicit waits
   - Element not clickable: Check for overlays or visibility
   - Form validation: Look for error messages
   - Timing issues: Use WebDriverWait, not time.sleep()

10. REALISTIC USER SIMULATION
    - Add small delays between actions (0.3-1 second)
    - Don't fill forms too fast (mimic human speed)
    - Interact with page like a real user would
    - Read error messages and respond appropriately

11. WORKFLOW CHAINS
    - Break complex workflows into logical steps
    - Use try/except to handle failures gracefully
    - Print status at each step for debugging
    - Verify expected state after each action

12. COMMON CHALLENGES & SOLUTIONS
    Problem: "Element is not clickable at point (x, y)"
    Solution: Scroll into view, wait for visibility, check for overlays
    
    Problem: "Stale Element Reference"
    Solution: Find element again, don't reuse element after page change
    
    Problem: "Element not interactable"
    Solution: Use JavaScript click or ActionChains
    
    Problem: Form submission doesn't work
    Solution: Verify all required fields filled, check for validation errors
    
    Problem: Dropdown won't open
    Solution: Use Select class, ensure correct selector
    """)


def main():
    """
    Main program demonstrating form and element interaction.
    """
    print()
    print("=" * 70)
    print("Day 49 - Form Automation & Element Interaction".center(70))
    print("=" * 70)
    print()
    
    print("Master interactive web element handling with Selenium.\n")
    
    print("Core Skills Covered:")
    print("  - Clicking buttons, links, and checkboxes")
    print("  - Typing text into input fields")
    print("  - Sending special keyboard keys")
    print("  - Submitting forms programmatically")
    print("  - Selecting dropdown options")
    print("  - Building complex automation workflows")
    print("  - Simulating real user interactions\n")
    
    display_interaction_tips()
    
    print()
    print("=" * 70)
    print("Key Functions Available".center(70))
    print("=" * 70)
    print("""
CLICKING:
  - click_element(driver, locator_type, locator_value)
  - click_link_by_text(driver, link_text)
  - click_partial_link_text(driver, partial_text)

TEXT INPUT:
  - type_into_field(driver, locator_type, locator_value, text)
  - type_into_field_by_name(driver, field_name, text)
  - type_into_field_by_id(driver, element_id, text)
  - clear_input_field(driver, locator_type, locator_value)

KEYBOARD:
  - send_special_key(driver, locator_type, locator_value, key)
  - press_enter(driver, locator_type, locator_value)
  - press_tab(driver, locator_type, locator_value)
  - press_escape(driver)
  - send_keyboard_shortcut(driver, *keys)

FORMS:
  - submit_form(driver, locator_type, locator_value)
  - find_form_button(driver, form_selector, button_text)
  - fill_form_field(driver, field_name, value)
  - select_checkbox(driver, locator_type, locator_value)
  - unselect_checkbox(driver, locator_type, locator_value)
  - select_radio_button(driver, locator_type, locator_value)
  - select_dropdown_option(driver, dropdown_selector, option_value)

WORKFLOWS:
  - fill_signup_form(driver, first_name, last_name, email)
  - search_and_filter_workflow(driver, search_term, filter_option)
    """)
    
    print()
    print("=" * 70)
    print("Practice Sites (No Real Accounts)".center(70))
    print("=" * 70)
    print("""
These sites are designed for practicing automation safely:
  - https://practice-automation.com/
  - https://practice-automation.com/form-submission/
  - https://practice-automation.com/checkboxes/
  - https://practice-automation.com/dropdown/
  - https://practice-automation.com/text-inputs/

Use these instead of real websites to avoid:
  - Unnecessary bot traffic to production sites
  - Account lockouts due to unusual activity
  - Terms of Service violations
  - IP blocking for suspicious requests
    """)
    
    print()
    print("=" * 70)
    print("Real-World Applications".center(70))
    print("=" * 70)
    print("""
Web Testing:
  - Automated test suites for form validation
  - QA testing of user workflows
  - Regression testing

Data Entry Automation:
  - Bulk form submission
  - Data migration between systems
  - Automated report filling

Account Management:
  - Automated account creation
  - Profile updates
  - Mass password resets

Web Scraping (with JS):
  - Search and filter workflows
  - Pagination handling
  - Dynamic content extraction

Business Automation:
  - Invoice submission
  - Order processing
  - Feedback form filling

SEO and Marketing:
  - Search engine testing
  - Rank tracking automation
  - Competitor analysis
    """)
    
    print()
    print("=" * 70)
    print("⚠️  ETHICAL GUIDELINES".center(70))
    print("=" * 70)
    print("""
ALWAYS:
  ✓ Use automation for your own accounts
  ✓ Check Terms of Service before automating
  ✓ Use test sites for practice
  ✓ Add delays between actions to avoid overloading servers
  ✓ Respect rate limits and robots.txt
  ✓ Use legitimate APIs when available

NEVER:
  ✗ Automate login to other people's accounts
  ✗ Bypass security measures or CAPTCHAs
  ✗ Generate spam or fake submissions
  ✗ Violate website Terms of Service
  ✗ Overload servers with rapid requests
  ✗ Circumvent IP bans or geo-restrictions
    """)
    
    print()
    print("=" * 70)
    print("[INFO] Ready to automate forms and web interactions!".center(70))
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
