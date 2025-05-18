# Accessibility Testing Framework

A Python-Selenium based framework for testing web accessibility compliance with WCAG 2.0 standards.

## Overview

This framework provides automated testing of web pages for accessibility issues according to WCAG 2.0 guidelines. It uses Selenium for browser automation and axe-core for accessibility testing, along with custom manual checks for a comprehensive evaluation approach.

## Features

- Automated accessibility testing using axe-core integration
- Manual testing for critical WCAG 2.0 criteria
- Page Object Model implementation for better test maintainability
- Support for multiple browsers (Chrome, Firefox)
- HTML reports with screenshots of violations
- Interactive dashboard with test summaries
- Command-line interface for custom testing options
- Responsive design accessibility testing
- Tests for key WCAG 2.0 criteria:
  - Missing alt text for images (1.1.1)
  - Color contrast issues (1.4.3)
  - Form inputs without labels (3.3.2)
  - Keyboard accessibility (2.1.1)
  - Heading structure (1.3.1)

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
4. View the results in the generated dashboard:
```
reports/dashboard.html
```

## Using the CLI

The framework includes a command-line interface for running custom tests:

```
python accessibility_cli.py --url https://example.com --browser chrome --wcag AA
```

Available options:
- `--url` or `-u`: URL to test
- `--browser` or `-b`: Browser to use (chrome, firefox)
- `--headless`: Run in headless mode
- `--wcag` or `-w`: WCAG level to test (A, AA, AAA)
- `--rules` or `-r`: Specific rules to test (comma-separated)
- `--output` or `-o`: Output directory for reports
- `--dashboard`: Generate dashboard after tests

## Project Structure

```
accessibility-test-framework/
├── src/                          # Source code
│   ├── core/                     # Core functionality
│   │   ├── accessibility_scanner.py  # Main scanner with axe integration
│   │   └── webdriver_manager.py  # Browser driver handling
│   ├── pages/                    # Page objects
│   │   ├── base_page.py          # Base page object
│   │   └── accessibility_test_page.py  # Extended page with manual checks
│   └── utils/                    # Utilities
│       ├── report_utils.py       # Reporting functionality
│       └── dashboard.py          # Dashboard generator
├── tests/                        # Test files
│   ├── config.py                 # Test configuration
│   ├── test_accessibility.py     # Test cases
│   └── sites/                    # Test site definitions
│       └── test_sites.py         # Sample HTML with accessibility issues
├── reports/                      # Generated reports and screenshots
├── requirements.txt              # Dependencies
├── run_tests.py                  # Script to run tests
└── accessibility_cli.py          # Command-line interface
```

## Example Usage

```python
from src.core.webdriver_manager import setup_driver
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.accessibility_test_page import AccessibilityTestPage

# Setup driver
driver = setup_driver("chrome")

# Create scanner and page objects
scanner = AccessibilityScanner(driver)
page = AccessibilityTestPage(driver)

# Open page
page.open("https://example.com")

# Run automated scan
scanner.inject_axe()
results = scanner.run_full_scan()

# Run manual checks
manual_results = page.run_manual_accessibility_checks()

# Print violations
scanner.print_violation_summary(results)

# Clean up
driver.quit()
```

## Reports

The framework generates several types of reports:
- Individual HTML reports for each tested page
- Rule-specific reports for WCAG criteria
- Screenshot gallery of testing
- Interactive dashboard summarizing all tests

## License

MIT