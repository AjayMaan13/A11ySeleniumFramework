# This is the main file for our webdriver setup
# It handles browser setup and configuration

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
        
        # Setup and return the driver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    
    elif browser.lower() == "firefox":
        # Setup Firefox options
        options = webdriver.FirefoxOptions()
        
        # Add headless mode if needed
        if headless:
            options.add_argument("--headless")
        
        # Setup and return the driver
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        return driver
    
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