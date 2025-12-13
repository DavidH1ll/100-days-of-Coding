"""
Day 49 - Form Automation Examples 
Practical demonstrations of form and element interactions with Selenium

These examples show real-world usage patterns for automating web forms
and interactive elements. Use the practice sites to safely test these patterns.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time


# ============================================================================
# EXAMPLE 1: Basic Form Filling and Submission
# ============================================================================

def example_basic_form_submission():
    """
    Example: Fill and submit a simple form.
    
    Use Case: Sign up forms, contact forms, basic data entry
    Site: https://practice-automation.com/form-submission/
    """
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Form Submission".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        driver = webdriver.Chrome()
        driver.get("https://practice-automation.com/form-submission/")
        print("[INFO] Navigated to form submission page\n")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "fName"))
        )
        print("[OK] Form loaded\n")
        
        # Fill first name
        print("[STEP 1] Filling first name...")
        fname_field = driver.find_element(By.NAME, "fName")
        fname_field.clear()
        fname_field.send_keys("John")
        print("[OK] First name: John\n")
        
        # Fill last name
        print("[STEP 2] Filling last name...")
        lname_field = driver.find_element(By.NAME, "lName")
        lname_field.clear()
        lname_field.send_keys("Doe")
        print("[OK] Last name: Doe\n")
        
        # Fill email
        print("[STEP 3] Filling email...")
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys("john.doe@example.com")
        print("[OK] Email: john.doe@example.com\n")
        
        # Select message
        print("[STEP 4] Filling message...")
        message_field = driver.find_element(By.NAME, "message")
        message_field.clear()
        message_field.send_keys("Hello, this is a test message!")
        print("[OK] Message filled\n")
        
        # Submit form
        print("[STEP 5] Submitting form...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        
        # Scroll button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.5)
        
        # Click submit
        submit_btn.click()
        print("[OK] Form submitted!\n")
        
        # Wait for success message
        print("[STEP 6] Waiting for confirmation...")
        success = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "post-title"))
        )
        print("[OK] Success message received!\n")
        
        print("[SUCCESS] Form submission example completed!\n")
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}\n")
        
    finally:
        if driver:
            driver.quit()
            print("[INFO] Browser closed\n")


# ============================================================================
# EXAMPLE 2: Checkbox and Radio Button Handling
# ============================================================================

def example_checkbox_radio_handling():
    """
    Example: Select checkboxes and radio buttons.
    
    Use Case: Option selection, preference forms, agreement checkboxes
    Site: https://practice-automation.com/checkboxes/
    """
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Checkbox and Radio Button Handling".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        driver = webdriver.Chrome()
        driver.get("https://practice-automation.com/checkboxes/")
        print("[INFO] Navigated to checkbox page\n")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "cb1"))
        )
        print("[OK] Checkboxes loaded\n")
        
        # Find all checkboxes
        print("[STEP 1] Finding all checkboxes...")
        checkboxes = driver.find_elements(By.NAME, "cb1")
        print(f"[OK] Found {len(checkboxes)} checkboxes\n")
        
        # Select first and third checkboxes
        print("[STEP 2] Selecting specific checkboxes...")
        for i, checkbox in enumerate(checkboxes, 1):
            if i in [1, 3]:
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"[OK] Checkbox {i} selected")
        print()
        
        # Verify selections
        print("[STEP 3] Verifying selections...")
        for i, checkbox in enumerate(checkboxes, 1):
            status = "CHECKED" if checkbox.is_selected() else "UNCHECKED"
            print(f"[INFO] Checkbox {i}: {status}")
        print()
        
        # Find and click the submit button if available
        print("[STEP 4] Looking for submit button...")
        try:
            submit_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_btn.click()
            print("[OK] Submit button clicked\n")
            time.sleep(1)
        except:
            print("[INFO] No submit button found\n")
        
        print("[SUCCESS] Checkbox handling example completed!\n")
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}\n")
        
    finally:
        if driver:
            driver.quit()
            print("[INFO] Browser closed\n")


# ============================================================================
# EXAMPLE 3: Dropdown Selection
# ============================================================================

def example_dropdown_selection():
    """
    Example: Select options from dropdown menus.
    
    Use Case: Country selection, date selection, preference menus
    Site: https://practice-automation.com/dropdown/
    """
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Dropdown Selection".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        driver = webdriver.Chrome()
        driver.get("https://practice-automation.com/dropdown/")
        print("[INFO] Navigated to dropdown page\n")
        
        # Wait for dropdown to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "select-fruit"))
        )
        print("[OK] Dropdown loaded\n")
        
        # Select by value
        print("[STEP 1] Selecting option by value...")
        dropdown = driver.find_element(By.ID, "select-fruit")
        select = Select(dropdown)
        
        # Get all available options
        options = select.options
        print(f"[INFO] Available options:")
        for option in options:
            print(f"  - {option.text} (value: {option.get_attribute('value')})")
        print()
        
        # Select apple
        print("[STEP 2] Selecting 'Apple'...")
        select.select_by_text("Apple")
        selected = Select(dropdown).first_selected_option
        print(f"[OK] Selected: {selected.text}\n")
        
        # Wait a moment
        time.sleep(1)
        
        # Select by index
        print("[STEP 3] Selecting option by index (index 2)...")
        select.select_by_index(2)
        selected = Select(dropdown).first_selected_option
        print(f"[OK] Selected: {selected.text}\n")
        
        # Select by value
        print("[STEP 4] Selecting option by value...")
        try:
            select.select_by_value("banana")
            selected = Select(dropdown).first_selected_option
            print(f"[OK] Selected: {selected.text}\n")
        except:
            print("[INFO] Option not available\n")
        
        print("[SUCCESS] Dropdown selection example completed!\n")
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}\n")
        
    finally:
        if driver:
            driver.quit()
            print("[INFO] Browser closed\n")


# ============================================================================
# EXAMPLE 4: Text Input and Keyboard Interaction
# ============================================================================

def example_text_input_keyboard():
    """
    Example: Type text and use keyboard shortcuts.
    
    Use Case: Search boxes, form fields, text areas
    Site: https://practice-automation.com/text-inputs/
    """
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Text Input and Keyboard Interaction".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        # Setup
        driver = webdriver.Chrome()
        driver.get("https://practice-automation.com/text-inputs/")
        print("[INFO] Navigated to text input page\n")
        
        # Wait for input fields to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fullname"))
        )
        print("[OK] Text input fields loaded\n")
        
        # Type into first field
        print("[STEP 1] Typing into fullname field...")
        fullname_field = driver.find_element(By.ID, "fullname")
        fullname_field.send_keys("John Doe")
        print("[OK] Typed: John Doe\n")
        
        # Move to next field with TAB
        print("[STEP 2] Pressing TAB to move to next field...")
        fullname_field.send_keys(Keys.TAB)
        print("[OK] Moved to next field\n")
        
        # Type into email field
        print("[STEP 3] Typing email...")
        current_element = driver.switch_to.active_element
        current_element.send_keys("john@example.com")
        print("[OK] Typed: john@example.com\n")
        
        # Select all and copy (simulate)
        print("[STEP 4] Selecting all text...")
        current_element.send_keys(Keys.CONTROL + "a")
        print("[OK] Text selected\n")
        
        # Clear with delete
        print("[STEP 5] Clearing text with DELETE...")
        current_element.send_keys(Keys.DELETE)
        print("[OK] Text cleared\n")
        
        # Retype
        print("[STEP 6] Retyping email...")
        current_element.send_keys("newemail@example.com")
        print("[OK] Typed: newemail@example.com\n")
        
        # Get field value
        value = current_element.get_attribute("value")
        print(f"[INFO] Current field value: {value}\n")
        
        print("[SUCCESS] Text input example completed!\n")
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}\n")
        
    finally:
        if driver:
            driver.quit()
            print("[INFO] Browser closed\n")


# ============================================================================
# EXAMPLE 5: Multi-Step Workflow
# ============================================================================

def example_multi_step_workflow():
    """
    Example: Complete a multi-step form workflow.
    
    Use Case: Registration flows, checkout processes, multi-page forms
    """
    
    print("\n" + "="*70)
    print("EXAMPLE 5: Multi-Step Workflow Simulation".center(70))
    print("="*70 + "\n")
    
    print("[INFO] This example simulates a complete workflow:\n")
    print("WORKFLOW STEPS:")
    print("1. Load page")
    print("2. Fill basic info (name, email)")
    print("3. Select preferences (checkbox)")
    print("4. Choose option (dropdown)")
    print("5. Submit form")
    print("6. Verify submission\n")
    
    driver = None
    try:
        # Initialize
        driver = webdriver.Chrome()
        
        # STEP 1: Load primary form
        print("[STEP 1] Loading form page...")
        driver.get("https://practice-automation.com/form-submission/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "fName"))
        )
        print("[OK] Form page loaded\n")
        
        # STEP 2: Fill basic information
        print("[STEP 2] Entering personal information...")
        
        # First name
        fname = driver.find_element(By.NAME, "fName")
        fname.clear()
        fname.send_keys("Jane")
        time.sleep(0.3)
        
        # Last name
        lname = driver.find_element(By.NAME, "lName")
        lname.clear()
        lname.send_keys("Smith")
        time.sleep(0.3)
        
        # Email
        email = driver.find_element(By.NAME, "email")
        email.clear()
        email.send_keys("jane.smith@example.com")
        print("[OK] Personal info entered\n")
        
        # STEP 3: Fill message
        print("[STEP 3] Entering message...")
        message = driver.find_element(By.NAME, "message")
        message.clear()
        message.send_keys("This is an automated submission test.")
        time.sleep(0.3)
        print("[OK] Message entered\n")
        
        # STEP 4: Find and click submit
        print("[STEP 4] Submitting form...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.5)
        submit_btn.click()
        print("[OK] Form submitted\n")
        
        # STEP 5: Verify submission
        print("[STEP 5] Verifying submission...")
        success_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "post-title"))
        )
        print(f"[OK] Success message found\n")
        
        print("[SUCCESS] Multi-step workflow completed!\n")
        
    except Exception as e:
        print(f"[ERROR] Workflow failed: {e}\n")
        
    finally:
        if driver:
            time.sleep(2)  # Show result for 2 seconds
            driver.quit()
            print("[INFO] Browser closed\n")


# ============================================================================
# EXAMPLE 6: Error Handling and Recovery
# ============================================================================

def example_error_handling():
    """
    Example: Handle common automation errors gracefully.
    
    Use Case: Production automation, robust scripts, error recovery
    """
    
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Handling and Recovery".center(70))
    print("="*70 + "\n")
    
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.get("https://practice-automation.com/form-submission/")
        print("[INFO] Navigated to form page\n")
        
        # Error Handling Pattern 1: Element not found
        print("[PATTERN 1] Handling element not found...")
        try:
            nonexistent = driver.find_element(By.ID, "nonexistent-element")
        except Exception as e:
            print(f"[OK] Caught error: {type(e).__name__}")
            print("[OK] Using alternative locator...\n")
        
        # Error Handling Pattern 2: Timeout waiting for element
        print("[PATTERN 2] Handling wait timeout...")
        try:
            element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "ghost-element"))
            )
        except Exception as e:
            print(f"[OK] Caught timeout: {type(e).__name__}")
            print("[OK] Retrying with different strategy...\n")
        
        # Error Handling Pattern 3: Element not clickable
        print("[PATTERN 3] Handling element not clickable...")
        try:
            fname = driver.find_element(By.NAME, "fName")
            # Try regular click
            try:
                fname.click()
            except:
                # Fallback to JavaScript click
                print("[OK] Regular click failed, using JavaScript...")
                driver.execute_script("arguments[0].click();", fname)
            print("[OK] Element clicked successfully\n")
        except Exception as e:
            print(f"[ERROR] Failed: {e}\n")
        
        # Error Handling Pattern 4: Form validation
        print("[PATTERN 4] Checking for validation errors...")
        errors = driver.find_elements(By.CLASS_NAME, "error-message")
        if errors:
            print(f"[WARNING] Found {len(errors)} validation errors:")
            for error in errors:
                print(f"  - {error.text}")
        else:
            print("[OK] No validation errors\n")
        
        # Error Handling Pattern 5: Retry pattern
        print("[PATTERN 5] Implementing retry pattern...")
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[ATTEMPT {attempt}] Trying to find element...")
                elem = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.NAME, "fName"))
                )
                print("[OK] Element found!\n")
                break
            except Exception as e:
                if attempt < max_retries:
                    print(f"[RETRY] Attempt {attempt} failed, retrying...\n")
                    time.sleep(1)
                else:
                    print(f"[ERROR] All {max_retries} attempts failed\n")
        
        print("[SUCCESS] Error handling examples completed!\n")
        
    except Exception as e:
        print(f"[ERROR] Example failed: {e}\n")
        
    finally:
        if driver:
            driver.quit()
            print("[INFO] Browser closed\n")


# ============================================================================
# Main Menu
# ============================================================================

def main():
    """
    Main menu to run examples.
    """
    print()
    print("="*70)
    print("Day 49 - Form Automation Examples".center(70))
    print("="*70)
    print("""
Choose an example to run:
1. Basic Form Submission
2. Checkbox and Radio Button Handling
3. Dropdown Selection
4. Text Input and Keyboard Interaction
5. Multi-Step Workflow
6. Error Handling and Recovery
7. Run All Examples
0. Exit

Note: Some examples open real websites. Make sure you have:
- ChromeDriver installed and in PATH
- Internet connection
- Chrome browser installed
    """)
    
    print("\nAvailable Examples:")
    print("- Example 1: Basic form filling and submission")
    print("- Example 2: Selecting checkboxes and radio buttons")
    print("- Example 3: Dropdown menu interaction")
    print("- Example 4: Text input and keyboard shortcuts")
    print("- Example 5: Multi-step workflow automation")
    print("- Example 6: Error handling patterns\n")
    
    print("To run an example, modify this file to call the desired function.")
    print("For example, uncomment the line below to run Example 1:\n")
    print("# example_basic_form_submission()\n")
    
    print("Or run from Python REPL:")
    print(">>> from example_usage import example_basic_form_submission")
    print(">>> example_basic_form_submission()\n")


if __name__ == "__main__":
    main()
    
    # Uncomment one or more examples to run them:
    # example_basic_form_submission()
    # example_checkbox_radio_handling()
    # example_dropdown_selection()
    # example_text_input_keyboard()
    # example_multi_step_workflow()
    # example_error_handling()
