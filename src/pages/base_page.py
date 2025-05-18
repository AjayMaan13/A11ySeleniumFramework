# Base page object that all page objects will inherit from

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver):
        """
        Initialize base page
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        # Default wait time in seconds
        self.timeout = 10
    
    def open(self, url):
        """
        Open the given URL
        
        Args:
            url: URL to open
        """
        self.driver.get(url)
    
    def get_title(self):
        """
        Get page title
        
        Returns:
            Page title
        """
        return self.driver.title
    
    def get_url(self):
        """
        Get current URL
        
        Returns:
            Current URL
        """
        return self.driver.current_url
    
    def find_element(self, locator_type, locator_value):
        """
        Find element using given locator
        
        Args:
            locator_type: By.XXX (eg. By.ID, By.CSS_SELECTOR)
            locator_value: Locator value
        
        Returns:
            WebElement if found, None otherwise
        """
        try:
            return self.driver.find_element(locator_type, locator_value)
        except NoSuchElementException:
            print(f"Element not found with {locator_type}: {locator_value}")
            return None
    
    def find_elements(self, locator_type, locator_value):
        """
        Find all elements using given locator
        
        Args:
            locator_type: By.XXX (eg. By.ID, By.CSS_SELECTOR)
            locator_value: Locator value
        
        Returns:
            List of WebElements if found, empty list otherwise
        """
        return self.driver.find_elements(locator_type, locator_value)
    
    def wait_for_element(self, locator_type, locator_value, timeout=None):
        """
        Wait for element to be present
        
        Args:
            locator_type: By.XXX (eg. By.ID, By.CSS_SELECTOR)
            locator_value: Locator value
            timeout: Timeout in seconds
        
        Returns:
            WebElement if found, None otherwise
        """
        if timeout is None:
            timeout = self.timeout
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator_value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with {locator_type}: {locator_value}")
            return None
    
    def check_accessibility(self, scanner):
        """
        Check accessibility of current page
        
        Args:
            scanner: AccessibilityScanner instance
        
        Returns:
            Dictionary with accessibility results
        """
        # Inject axe-core into page
        scanner.inject_axe()
        
        # Run scan
        results = scanner.run_full_scan()
        
        return results