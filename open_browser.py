"""
Simple script to open a web page using Selenium
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def open_webpage(url):
    """Open a webpage in Chrome browser"""
    
    # Setup Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment to run without GUI
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"Opening URL: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        print(f"Page title: {driver.title}")
        print("Browser will stay open for 10 seconds...")
        time.sleep(10)
        
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    url = "https://www.tiktok.com/signup/phone-or-email/email"
    open_webpage(url)
