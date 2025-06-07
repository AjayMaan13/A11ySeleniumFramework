# ♿ Accessibility Testing Framework

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-4.x-green)
![WCAG](https://img.shields.io/badge/WCAG-2.0-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Comprehensive Python-Selenium framework for automated web accessibility testing against WCAG 2.0 and AODA standards with cross-browser support and visual reporting.

## 🎯 Features

- 🔍 **Automated Scanning** - axe-core integration for comprehensive WCAG 2.0 compliance
- 🧩 **Page Object Model** - Maintainable test architecture with reusable components
- 🌈 **Cross-Browser Support** - Firefox and Chrome compatibility with CI/CD integration
- 📊 **Visual Reporting** - Screenshots and evidence with detailed violation documentation
- 📱 **Responsive Testing** - Multi-device accessibility validation
- 🔄 **GitHub Actions** - Continuous testing across development workflows

## 🛠️ Tech Stack

**Core:** Python 3.9+, Selenium WebDriver, PyTest framework  
**Accessibility:** axe-core accessibility engine for WCAG 2.0 validation  
**Testing:** Page Object Model architecture, cross-browser automation  
**Reporting:** Visual documentation with screenshots and compliance metrics

## ✅ WCAG Criteria Coverage (POUR Methodology)

**Perceivable**
- **1.1.1 Non-text Content** - Images have text alternatives
- **1.4.3 Contrast** - Sufficient color contrast validation

**Operable**  
- **2.1.1 Keyboard** - Keyboard accessibility verification

**Understandable**
- **3.3.2 Labels** - Form elements have proper labels

**Robust**
- **1.3.1 Info & Relationships** - Proper heading structure

## 🚀 Quick Start

### Installation & Setup
```bash
git clone https://github.com/AjayMaan13/A11ySeleniumFramework.git
cd A11ySeleniumFramework
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Running Tests
```bash
# Run comprehensive test suite
python run_tests.py

# Test specific URL with options
python accessibility_cli.py --url https://example.com --browser firefox --wcag AA

# View generated dashboard
open reports/dashboard.html
```

## 📁 Structure

```
A11ySeleniumFramework/
├── src/
│   ├── core/
│   │   ├── accessibility_scanner.py  # axe-core integration
│   │   └── webdriver_manager.py      # Browser management
│   ├── pages/
│   │   ├── base_page.py              # Page Object base
│   │   └── accessibility_test_page.py # Extended validation
│   └── utils/
│       ├── dashboard.py              # Report generation
│       └── wcag_reference.py         # Guidelines reference
├── tests/
│   ├── test_accessibility.py        # Main test cases
│   └── config.py                     # Test configuration
├── .github/workflows/
│   └── accessibility-tests.yml      # CI/CD pipeline
└── reports/                          # Generated reports
```

## 🏗️ Architecture

### Core Implementation
```python
# Main testing workflow
from src.core.accessibility_scanner import AccessibilityScanner
from src.pages.accessibility_test_page import AccessibilityTestPage

# Setup and execute tests
driver = setup_driver("firefox")
scanner = AccessibilityScanner(driver)
page = AccessibilityTestPage(driver)

# Run comprehensive accessibility scan
page.open("https://example.com")
scanner.inject_axe()
results = scanner.run_full_scan()
```
## 🧪 Testing & CI/CD

```bash
# Cross-browser testing
python accessibility_cli.py --browser firefox  # Recommended for macOS
python accessibility_cli.py --browser chrome   # Windows/Linux

# GitHub Actions integration for continuous accessibility testing
```

## 📈 Performance Metrics

- **100% test coverage** across critical accessibility requirements
- **Cross-browser compatibility** with Firefox and Chrome
- **Automated CI/CD** integration with GitHub Actions
- **Visual reporting** with comprehensive violation documentation

## 👨‍💻 Author

**Ajaypartap Singh Maan**  
[GitHub](https://github.com/AjayMaan13) • [LinkedIn](https://linkedin.com/in/ajaypartap-singh-maan) • ajayapsmaanm13@gmail.com

---

⭐ **Star if helpful!**
