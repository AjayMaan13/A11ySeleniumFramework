# 🌐 Accessibility Testing Framework

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-4.x-green)
![WCAG](https://img.shields.io/badge/WCAG-2.0-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A comprehensive Python-Selenium framework for automated web accessibility testing against WCAG 2.0 standards.

## ✨ Features

- 🔍 **Automated Scanning** with axe-core integration
- 🖐️ **Manual Testing** for critical WCAG 2.0 criteria
- 🧩 **Page Object Model** for maintainable test architecture
- 🌈 **Cross-browser Support** (Firefox recommended, Chrome supported)
- 📊 **Visual Reporting** with screenshots and evidence
- 📱 **Responsive Testing** across device sizes
- 🔄 **CI/CD Integration** with GitHub Actions
- 💻 **Command-line Interface** for custom testing

## 📋 WCAG Criteria Tested

- ✅ **1.1.1 Non-text Content** - Images have text alternatives
- ✅ **1.4.3 Contrast** - Text has sufficient color contrast
- ✅ **3.3.2 Labels** - Form elements have proper labels
- ✅ **2.1.1 Keyboard** - All functions accessible by keyboard
- ✅ **1.3.1 Info & Relationships** - Proper heading structure

## 🚀 Quick Start

### Installation

```
# Clone the repository
git clone https://github.com/yourusername/accessibility-testing-framework.git
cd accessibility-testing-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```
# Run all tests with dashboard generation
python run_tests.py

# Test a specific URL
python accessibility_cli.py --url https://example.com

# Run with options (Firefox recommended for macOS with Apple Silicon)
python accessibility_cli.py --browser firefox --wcag AA --headless
```

### Viewing Results

After running tests, open the dashboard:
```
open reports/dashboard.html  # On macOS
# Or simply open the file in your browser
```

## 📁 Project Structure

```
accessibility-test-framework/
├── .github/                      # GitHub configurations
│   └── workflows/                # GitHub Actions workflows
│       └── accessibility-tests.yml  # CI pipeline configuration
├── src/                          # Source code
│   ├── core/                     # Core functionality
│   │   ├── __init__.py           # Package initializer
│   │   ├── accessibility_scanner.py  # Main scanner with axe integration
│   │   └── webdriver_manager.py  # Browser driver management
│   ├── pages/                    # Page objects
│   │   ├── __init__.py           # Package initializer
│   │   ├── base_page.py          # Base page object
│   │   └── accessibility_test_page.py  # Extended page with manual checks
│   └── utils/                    # Utilities
│       ├── __init__.py           # Package initializer
│       ├── dashboard.py          # Dashboard generator
│       ├── report_utils.py       # Reporting tools
│       └── wcag_reference.py     # WCAG guidelines reference
├── tests/                        # Test files
│   ├── __init__.py               # Package initializer
│   ├── config.py                 # Test configuration
│   ├── test_accessibility.py     # Main test cases
│   └── sites/                    # Test site definitions
│       ├── __init__.py           # Package initializer
│       └── test_sites.py         # Sample HTML generators
├── reports/                      # Generated reports
│   └── screenshots/              # Screenshot storage
│       └── .gitkeep              # Placeholder for empty dir
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT license file
├── README.md                     # Project documentation
├── CONTRIBUTING.md               # Contribution guidelines
├── DOCUMENTATION.md              # User documentation
├── accessibility_cli.py          # Command-line interface
├── example.py                    # Example usage
├── requirements.txt              # Dependencies
└── run_tests.py                  # Test runner script
```

## 🛠️ Advanced Usage

### Custom Test Rules

Define specific WCAG rules to test:
```
python accessibility_cli.py --rules "image-alt,color-contrast,keyboard"
```

### Cross-browser Testing

Test on different browsers:
```
# Firefox (recommended for macOS with Apple Silicon)
python accessibility_cli.py --browser firefox

# Chrome (on Windows/Linux or with manual ChromeDriver installation)
python accessibility_cli.py --browser chrome
```

### Responsive Testing

Test at different viewport sizes:
```
python run_tests.py
# The responsive tests are included by default
```

## 📊 Sample Reports

The framework generates comprehensive reports including:

- 📈 Summary dashboard with test metrics
- 📷 Screenshots of violations
- 🔍 Detailed rule explanations
- 📱 Responsive testing results
- 🔗 Links to WCAG documentation

## 🖥️ Browser Compatibility

- **Firefox**: Primary recommended browser, works on all platforms including macOS with Apple Silicon
- **Chrome**: Works on Windows/Linux. For macOS with Apple Silicon, requires manual ChromeDriver installation:
  ```
  brew install --cask chromedriver
  xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
  ```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

For detailed usage, see [DOCUMENTATION.md](DOCUMENTATION.md).

## 📝 Example Usage

```python
from src.core.webdriver_manager import setup_driver
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.accessibility_test_page import AccessibilityTestPage

# Setup Firefox driver (recommended for macOS)
driver = setup_driver("firefox")

# Create scanner and page objects
scanner = AccessibilityScanner(driver)
page = AccessibilityTestPage(driver)

# Test a website
page.open("https://example.com")
scanner.inject_axe()
results = scanner.run_full_scan()

# Print violations
scanner.print_violation_summary(results)
```

## 📃 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

💡 **Why Accessibility Matters**: Making the web accessible ensures equal access and opportunity for people with diverse abilities, improving user experience for everyone.