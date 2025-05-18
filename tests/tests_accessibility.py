# Main accessibility test file

import os
import pytest
import time
from pathlib import Path

# Import from our project
from src.core.webdriver_manager import setup_driver, teardown_driver
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.base_page import BasePage
from src.utils.report_utils import take_screenshot, highlight_element, generate_simple_report

# Import configuration
from tests.config import TEST_URLS, BROWSER, HEADLESS, AXE_RULES
from tests.sites.test_sites import create_test_pages


# Create local test pages before running tests
@pytest.fixture(scope="session", autouse=True)
def setup_test_pages():
    """Create local test pages for testing"""
    # Create the test pages
    created_files = create_test_pages()
    
    # Get absolute paths for local files
    local_files = []
    for file in created_files:
        abs_path = os.path.abspath(file)
        # Convert to file:// URL format
        file_url = f"file://{abs_path}"
        local_files.append(file_url)
    
    # Update the local URLs in TEST_URLS
    TEST_URLS["local"] = local_files
    
    yield
    
    # No cleanup needed - files will be overwritten on next run


# Setup and teardown for webdriver
@pytest.fixture
def driver():
    """Setup and teardown for WebDriver"""
    # Setup driver
    driver = setup_driver(BROWSER, HEADLESS)
    
    # Set window size and position
    driver.set_window_size(1366, 768)
    
    yield driver
    
    # Teardown
    teardown_driver(driver)


# Test accessibility on public sites
@pytest.mark.parametrize("url", TEST_URLS["public"])
def test_public_site_accessibility(driver, url):
    """Test accessibility on public websites"""
    # Create scanner and page objects
    scanner = AccessibilityScanner(driver)
    page = BasePage(driver)
    
    # Navigate to the test URL
    page.open(url)
    
    # Let page load completely
    time.sleep(2)
    
    # Run accessibility scan
    try:
        # Inject axe-core
        scanner.inject_axe()
        
        # Run scan with standard rules
        results = scanner.run_full_scan()
        
        # Generate basic report
        report_path = f"reports/accessibility_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.html"
        generate_simple_report(results, report_path)
        
        # Print summary of violations
        scanner.print_violation_summary(results)
        
        # Take screenshot of the page
        screenshot_path = take_screenshot(driver, filename=f"screenshot_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png")
        
        # Count violations
        violations = scanner.get_violations(results)
        
        # Assert that number of violations is reported (not necessarily zero)
        assert isinstance(violations, list), "Violations should be a list"
        
        # Log the number of violations
        print(f"Found {len(violations)} accessibility violations on {url}")
        
    except Exception as e:
        # If there's an error, take screenshot and fail test
        take_screenshot(driver, filename=f"error_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png")
        pytest.fail(f"Error testing {url}: {e}")


# Test accessibility on local files
@pytest.mark.parametrize("url", TEST_URLS["local"])
def test_local_site_accessibility(driver, url):
    """Test accessibility on local test pages"""
    # Create scanner and page objects
    scanner = AccessibilityScanner(driver)
    page = BasePage(driver)
    
    # Navigate to the test URL
    page.open(url)
    
    # Let page load completely
    time.sleep(1)
    
    # Run accessibility scan
    try:
        # Inject axe-core
        scanner.inject_axe()
        
        # Create a custom set of rules to check
        custom_options = {
            'runOnly': {
                'type': 'tag',
                'values': ['wcag2a', 'wcag2aa']
            }
        }
        
        # Run scan with custom options
        results = scanner.run_custom_scan(options=custom_options)
        
        # Generate detailed report
        filename = Path(url).name
        report_path = f"reports/accessibility_{filename}.html"
        generate_simple_report(results, report_path)
        
        # Print summary of violations
        scanner.print_violation_summary(results)
        
        # Take screenshot of the page
        screenshot_path = take_screenshot(driver, filename=f"screenshot_{filename}.png")
        
        # Count violations
        violations = scanner.get_violations(results)
        
        # For local files, we expect specific violations
        if "missing_alt" in url:
            # Check for alt text violations
            alt_violations = [v for v in violations if v.get('id') == 'image-alt']
            assert len(alt_violations) > 0, "Should have alt text violations"
            
        elif "contrast_issues" in url:
            # Check for contrast violations
            contrast_violations = [v for v in violations if v.get('id') == 'color-contrast']
            assert len(contrast_violations) > 0, "Should have contrast violations"
            
        elif "form_labels" in url:
            # Check for form label violations
            label_violations = [v for v in violations if v.get('id') == 'label']
            assert len(label_violations) > 0, "Should have label violations"
        
    except Exception as e:
        # If there's an error, take screenshot and fail test
        take_screenshot(driver, filename=f"error_{Path(url).name}.png")
        pytest.fail(f"Error testing {url}: {e}")


# Test specific WCAG rules
@pytest.mark.parametrize("rule", AXE_RULES["essential"])
def test_specific_wcag_rule(driver, rule):
    """Test specific WCAG rules across test pages"""
    # Use the first local test page for this test
    url = TEST_URLS["local"][0]
    
    # Create scanner and page objects
    scanner = AccessibilityScanner(driver)
    page = BasePage(driver)
    
    # Navigate to the test URL
    page.open(url)
    
    # Let page load completely
    time.sleep(1)
    
    # Run accessibility scan for specific rule
    try:
        # Inject axe-core
        scanner.inject_axe()
        
        # Create a custom set of rules to check just this rule
        custom_options = {
            'runOnly': {
                'type': 'rule',
                'values': [rule]
            }
        }
        
        # Run scan with custom options
        results = scanner.run_custom_scan(options=custom_options)
        
        # Generate report
        report_path = f"reports/rule_{rule}.html"
        generate_simple_report(results, report_path)
        
        # Print summary of violations
        scanner.print_violation_summary(results)
        
        # Take screenshot of the page
        screenshot_path = take_screenshot(driver, filename=f"rule_{rule}.png")
        
        # Count violations
        violations = scanner.get_violations(results)
        
        # Assert that results were returned (not checking pass/fail)
        assert results is not None, f"Should get results for rule {rule}"
        
        # Log the result
        print(f"Tested rule {rule} with {len(violations)} violations")
        
    except Exception as e:
        # If there's an error, take screenshot and fail test
        take_screenshot(driver, filename=f"error_rule_{rule}.png")
        pytest.fail(f"Error testing rule {rule}: {e}")


# Main function for running tests directly
if __name__ == "__main__":
    # Run all tests with HTML report generation
    pytest.main(["-v", "--html=reports/report.html"])