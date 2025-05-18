# Demo documentation page that explains how to use the framework
# This file can be included in your project to make it more user-friendly

# Documentation for Accessibility Testing Framework

## Quick Start

```python
# Example code to show basic usage
from src.core.webdriver_manager import setup_driver
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.accessibility_test_page import AccessibilityTestPage

# Setup WebDriver
driver = setup_driver("chrome")

# Create scanner and page objects
scanner = AccessibilityScanner(driver)
page = AccessibilityTestPage(driver)

# Test a website
page.open("https://example.com")
scanner.inject_axe()
results = scanner.run_full_scan()

# Print violations
scanner.print_violation_summary(results)

# Run manual checks
manual_results = page.run_manual_accessibility_checks()

# Clean up
driver.quit()
```

## Key WCAG 2.0 Guidelines Tested

This framework tests for compliance with the following important WCAG 2.0 guidelines:

1. **1.1.1 Non-text Content** (Level A)
   - All images must have alt text
   - Meaningful images need descriptive alt text
   - Decorative images should have empty alt text

2. **1.4.3 Contrast** (Level AA)
   - Text must have sufficient contrast with its background
   - Regular text: minimum ratio of 4.5:1
   - Large text: minimum ratio of 3:1

3. **3.3.2 Labels or Instructions** (Level A)
   - All form controls must have associated labels
   - Instructions for user input should be clear

4. **2.1.1 Keyboard** (Level A)
   - All functionality must be available via keyboard
   - No keyboard traps should exist

5. **1.3.1 Info and Relationships** (Level A)
   - Heading structure must be logical
   - Form elements must have proper labels

## Interpreting Test Results

The framework generates HTML reports that include:

- Summary of violations by category
- Screenshots of problematic elements
- Details on each violation with suggestions for fixing

### Example Violations

#### Missing Alt Text
```html
<!-- Bad Example -->
<img src="logo.png">

<!-- Good Example -->
<img src="logo.png" alt="Company Logo">
```

#### Poor Contrast
```css
/* Bad Example */
.low-contrast {
  color: #aaa;
  background-color: #eee;
}

/* Good Example */
.good-contrast {
  color: #000;
  background-color: #fff;
}
```

#### Form Without Labels
```html
<!-- Bad Example -->
<input type="text" placeholder="Enter your name">

<!-- Good Example -->
<label for="name">Name</label>
<input type="text" id="name">
```

## Command Line Options

The `accessibility_cli.py` script accepts the following arguments:

```
python accessibility_cli.py --url https://example.com --browser chrome --wcag AA
```

- `--url` or `-u`: URL to test
- `--browser` or `-b`: Browser to use (chrome, firefox)
- `--headless`: Run in headless mode
- `--wcag` or `-w`: WCAG level to test (A, AA, AAA)
- `--rules` or `-r`: Specific rules to test (comma-separated)
- `--output` or `-o`: Output directory for reports
- `--dashboard`: Generate dashboard after tests