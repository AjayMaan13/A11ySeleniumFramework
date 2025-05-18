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
- 🌈 **Multi-browser Support** (Chrome, Firefox)
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

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```
# Run all tests with dashboard generation
python run_tests.py

# Test a specific URL
python accessibility_cli.py --url https://example.com

# Run with options
python accessibility_cli.py --browser chrome --wcag AA --headless
```

### Viewing Results

After running tests, open the dashboard:
```
reports/dashboard.html
```

## 📁 Project Structure

```
accessibility-test-framework/
├── src/                            # Source code
│   ├── core/                       # Core functionality
│   │   ├── accessibility_scanner.py  # Main scanner with axe integration
│   │   └── webdriver_manager.py    # Browser driver handling
│   ├── pages/                      # Page objects
│   │   ├── base_page.py            # Base page object
│   │   └── accessibility_test_page.py  # Extended page with manual checks
│   └── utils/                      # Utilities
│       ├── report_utils.py         # Reporting functionality
│       ├── dashboard.py            # Dashboard generator
│       └── wcag_reference.py       # WCAG guidelines reference
├── tests/                          # Test files
│   ├── config.py                   # Test configuration
│   ├── test_accessibility.py       # Test cases
│   └── sites/                      # Test site definitions
│       └── test_sites.py           # Sample HTML with accessibility issues
├── reports/                        # Generated reports and screenshots
│   └── screenshots/                # Screenshot directory with .gitkeep
├── .github/workflows/              # GitHub Actions configuration
│   └── accessibility-tests.yml     # CI workflow
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
├── DOCUMENTATION.md                # Detailed documentation
├── run_tests.py                    # Script to run tests
├── accessibility_cli.py            # Command-line interface
├── example.py                      # Example usage script
└── README.md                       # Project overview with badges and emoji
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
python accessibility_cli.py --browser firefox
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

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

For detailed usage, see [DOCUMENTATION.md](DOCUMENTATION.md).

## 📃 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

💡 **Why Accessibility Matters**: Making the web accessible ensures equal access and opportunity for people with diverse abilities, improving user experience for everyone.