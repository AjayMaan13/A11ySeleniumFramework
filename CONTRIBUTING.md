# Contributing Guidelines

Thank you for your interest in contributing to the Accessibility Testing Framework! This document will guide you through the process of contributing to this project.

## Development Setup

1. Fork the repository and clone it to your local machine
2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Install development dependencies:
```
pip install pytest-cov flake8
```

## Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Keep functions small and focused
- Write unit tests for new functionality

## Pull Request Process

1. Create a new branch for your feature or bugfix
2. Make your changes and commit them with clear, descriptive messages
3. Run tests to ensure everything is working:
```
python run_tests.py
```
4. Push your branch and submit a pull request
5. Describe the changes you've made and any relevant information

## Adding New WCAG Tests

When adding new accessibility tests:

1. Check if the test can be performed using axe-core
2. If not, implement a manual test in the `AccessibilityTestPage` class
3. Document the WCAG guideline being tested
4. Add test cases to `test_accessibility.py`

## Report Bugs

If you find a bug, please create an issue with:

- A clear description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Environment information (browser, OS, etc.)

## Feature Requests

Feature requests are welcome! Please create an issue describing:

- The feature you'd like to see
- Why it would be valuable
- Any implementation ideas you have

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive community