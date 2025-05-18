# This is the main file for our webdriver setup
# It handles browser setup and configuration

import os
import platform
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def setup_driver(browser="chrome", headless=False):
    """
    Setup and configure WebDriver
    
    Args:
        browser: Browser to use (chrome or firefox)
        headless: Run in headless mode or not
    
    Returns:
        WebDriver instance
    """
    if browser.lower() == "chrome":
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        
        # Add headless mode if needed
        if headless:
            options.add_argument("--headless")
        
        # Add some default arguments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        try:
            # For Mac with Apple Silicon (M1/M2/M3)
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                print("Detected Mac with Apple Silicon. Setting up appropriate ChromeDriver.")
                # Use Chrome driver directly without webdriver_manager
                # Try to find the chromedriver binary directly 
                chrome_service = ChromeService("/opt/homebrew/bin/chromedriver")
                driver = webdriver.Chrome(service=chrome_service, options=options)
            else:
                # Standard setup for other platforms
                chrome_service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=chrome_service, options=options)
            
            return driver
        except Exception as e:
            print(f"Error setting up Chrome: {e}")
            print("Trying Firefox instead...")
            return setup_driver("firefox", headless)
    
    elif browser.lower() == "firefox":
        # Setup Firefox options
        options = webdriver.FirefoxOptions()
        
        # Add headless mode if needed
        if headless:
            options.add_argument("--headless")
        
        try:
            # Setup and return the driver
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            return driver
        except Exception as e:
            print(f"Error setting up Firefox: {e}")
            print("Please install Firefox or Chrome manually.")
            sys.exit(1)
    
    else:
        # If we get an unsupported browser, default to Chrome
        print(f"Browser {browser} not supported. Using Chrome instead.")
        return setup_driver("chrome", headless)


def teardown_driver(driver):
    """
    Clean up webdriver instance
    
    Args:
        driver: WebDriver instance to clean up
    """
    if driver:
        driver.quit()