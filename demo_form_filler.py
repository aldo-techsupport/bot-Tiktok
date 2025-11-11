"""
Demo: Automated form filling using Selenium
Uses a public testing website - safe and legal to practice on
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
import random
import string

def generate_random_email():
    """Generate a random email address"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@example.com"

def generate_random_password():
    """Generate a random password"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def fill_demo_form():
    """
    Fill out a demo registration form automatically
    Using: https://www.selenium.dev/selenium/web/web-form.html
    """
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')  # Uncomment to run without GUI
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Opening demo form page...")
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        print("Filling form fields...")
        
        # Fill Text Input
        text_input = wait.until(EC.presence_of_element_located((By.ID, "my-text-id")))
        text_input.send_keys("John Doe")
        print("✓ Text input filled")
        
        # Fill Password
        password_input = driver.find_element(By.NAME, "my-password")
        random_password = generate_random_password()
        password_input.send_keys(random_password)
        print(f"✓ Password filled: {random_password}")
        
        # Fill Textarea
        textarea = driver.find_element(By.NAME, "my-textarea")
        textarea.send_keys("This is an automated test for learning purposes.")
        print("✓ Textarea filled")
        
        # Select Dropdown
        dropdown = Select(driver.find_element(By.NAME, "my-select"))
        dropdown.select_by_index(2)  # Select option 2
        print("✓ Dropdown selected")
        
        # Fill Date Picker
        date_input = driver.find_element(By.NAME, "my-date")
        date_input.send_keys("11/11/1995")
        print("✓ Date filled")
        
        # Check Checkbox 1
        checkbox1 = driver.find_element(By.ID, "my-check-1")
        if not checkbox1.is_selected():
            checkbox1.click()
        print("✓ Checkbox 1 checked")
        
        # Check Checkbox 2
        checkbox2 = driver.find_element(By.ID, "my-check-2")
        if not checkbox2.is_selected():
            checkbox2.click()
        print("✓ Checkbox 2 checked")
        
        # Select Radio Button
        radio = driver.find_element(By.ID, "my-radio-2")
        radio.click()
        print("✓ Radio button selected")
        
        # Fill Color Picker
        color_picker = driver.find_element(By.NAME, "my-colors")
        driver.execute_script("arguments[0].value = '#FF5733';", color_picker)
        print("✓ Color picker set")
        
        # Fill Range Slider
        range_slider = driver.find_element(By.NAME, "my-range")
        driver.execute_script("arguments[0].value = '7';", range_slider)
        print("✓ Range slider set")
        
        print("\n✅ All form fields filled successfully!")
        print("Form will be submitted in 5 seconds...")
        time.sleep(5)
        
        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        print("✓ Form submitted")
        
        # Wait to see the result
        time.sleep(3)
        
        # Check if we're on the success page
        if "Received!" in driver.page_source:
            print("✅ Form submission successful!")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nClosing browser...")
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: Automated Form Filling with Selenium")
    print("=" * 60)
    print("\nThis demo uses a public testing website.")
    print("It's safe and legal to practice automation here.\n")
    
    fill_demo_form()
