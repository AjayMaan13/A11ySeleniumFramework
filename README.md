# README.md for the project

# Accessibility Testing Framework

A Python-Selenium based framework for testing web accessibility compliance with WCAG 2.0 standards.

## Overview

This framework provides automated testing of web pages for accessibility issues according to WCAG 2.0 guidelines. It uses Selenium for browser automation and axe-core for accessibility testing.

## Features

- Automated accessibility testing using axe-core
- Page Object Model implementation for better test maintainability
- Support for multiple browsers (Chrome, Firefox)
- HTML reporting with screenshots of violations
- Tests for important WCAG 2.0 criteria:
  - Missing alt text for images (1.1.1)
  - Color contrast issues (1.4.3)
  - Form inputs without labels (3.3.2)
  - Keyboard accessibility (2.1.1)

## Setup

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the tests:
```
python run_tests.py
```

## Project Structure

```
accessibility-test-framework/
├── src/                          # Source code
│   ├── core/                     # Core functionality
│   │   ├── accessibility_scanner.py  # Main scanner
│   │   └── webdriver_manager.py  # Browser driver handling
│   ├── pages/                    # Page objects
│   │   └── base_page.py          # Base page object
│   └── utils/                    # Utilities
│       └── report_utils.py       # Reporting functionality
├── tests/                        # Test files
│   ├── config.py                 # Test configuration
│   └── test_accessibility.py     # Test cases
├── reports/                      # Generated reports
├── requirements.txt              # Dependencies
└── run_tests.py                  # Script to run tests
```

## Example Usage

```python
from src.core.webdriver_manager import setup_driver
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.base_page import BasePage

# Setup driver
driver = setup_driver("chrome")

# Create scanner
scanner = AccessibilityScanner(driver)

# Create page object
page = BasePage(driver)

# Open page
page.open("https://example.com")

# Test accessibility
results = page.check_accessibility(scanner)

# Print violations
scanner.print_violation_summary(results)

# Clean up
driver.quit()
```

## Reports

Reports are generated in the `reports` directory in HTML format, showing:
- Summary of accessibility violations
- Screenshots of elements with issues
- Details of each violation with WCAG references

## License

MIT