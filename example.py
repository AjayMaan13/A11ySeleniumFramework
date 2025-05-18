# Simple example showing how to use the framework

import time
from src.core.webdriver_manager import setup_driver, teardown_driver
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.accessibility_test_page import AccessibilityTestPage
from src.utils.report_utils import generate_simple_report
from src.utils.wcag_reference import get_wcag_explanation


def run_simple_example():
    """
    Simple example of using the accessibility testing framework
    """
    print("Running simple accessibility test example")
    print("=========================================")
    
    # Setup the WebDriver
    driver = setup_driver("chrome")
    
    try:
        # Create scanner and page objects
        scanner = AccessibilityScanner(driver)
        page = AccessibilityTestPage(driver)
        
        # Open a website to test
        url = "https://www.example.com"
        print(f"Testing accessibility of: {url}")
        page.open(url)
        
        # Let page load
        time.sleep(2)
        
        # Run accessibility scan
        print("Running accessibility scan...")
        scanner.inject_axe()
        results = scanner.run_full_scan()
        
        # Generate a report
        report_path = "reports/example_test.html"
        generate_simple_report(results, report_path)
        
        # Print summary of violations
        violations = scanner.get_violations(results)
        print(f"Found {len(violations)} accessibility violations.")
        
        # Print details of each violation with WCAG reference
        for i, violation in enumerate(violations, 1):
            violation_id = violation.get('id', 'Unknown')
            impact = violation.get('impact', 'unknown')
            nodes = len(violation.get('nodes', []))
            
            print(f"\nViolation {i}: {violation_id}")
            print(f"Impact: {impact}")
            print(f"Elements affected: {nodes}")
            
            # Get WCAG explanation if available
            wcag_tags = violation.get('tags', [])
            for tag in wcag_tags:
                if tag.startswith('wcag') and len(tag) > 5:
                    # Extract WCAG number (e.g., wcag2a-1.1.1 -> 1.1.1)
                    wcag_num = tag.split('-')[-1] if '-' in tag else None
                    if wcag_num:
                        explanation = get_wcag_explanation(wcag_num)
                        if explanation:
                            print(f"WCAG {wcag_num}: {explanation}")
        
        # Run manual checks
        print("\nRunning manual accessibility checks...")
        manual_results = page.run_manual_accessibility_checks()
        
        # Print manual check results
        print("\nManual check results:")
        print(f"Keyboard navigation possible: {manual_results['keyboard_navigation']['can_tab_through']}")
        print(f"Images with missing alt text: {manual_results['image_alt_text']['missing_alt']}")
        print(f"Form controls without labels: {manual_results['form_labels']['fields_without_labels']}")
        print(f"Proper heading structure: {manual_results['heading_structure']['proper_sequence']}")
        
        print("\nExample test complete!")
        print(f"Report generated at: {report_path}")
    
    finally:
        # Clean up
        teardown_driver(driver)


if __name__ == "__main__":
    run_simple_example()