# Test configuration file

# URLs to test - a mix of public sites and local files
TEST_URLS = {
    # Public sites known to have some accessibility issues
    "public": [
        "https://www.example.com",  # Simple site for testing
        "https://www.w3.org/WAI/demos/bad/",  # W3C's "Before and After" demo site
        "https://dequeuniversity.com/demo/mars/"  # Deque's Mars Commuter demo site
    ],
    
    # Local test files - these will be created in the tests/sites directory
    "local": [
        "file:///tests/sites/missing_alt.html",
        "file:///tests/sites/contrast_issues.html",
        "file:///tests/sites/form_labels.html"
    ]
}

# Browser configuration
BROWSER = "chrome"  # Options: "chrome", "firefox"
HEADLESS = False    # Run browser in headless mode

# Wait times
DEFAULT_TIMEOUT = 10  # Default timeout for finding elements (seconds)

# Accessibility test configuration
AXE_RULES = {
    # Essential rules to check (most critical WCAG guidelines)
    "essential": [
        "image-alt",           # Images must have alt text (WCAG 1.1.1)
        "label",               # Form elements must have labels (WCAG 3.3.2)
        "color-contrast",      # Text must have sufficient contrast (WCAG 1.4.3)
        "keyboard",            # Page must be keyboard accessible (WCAG 2.1.1)
    ],
    
    # Additional rules if time permits
    "additional": [
        "aria-roles",          # ARIA roles must be valid (WCAG 4.1.2)
        "heading-order",       # Headings must be in order (WCAG 1.3.1)
        "link-name",           # Links must have discernible text (WCAG 2.4.4)
        "region",              # Content should be inside landmarks (Best practice)
    ]
}

# Report configuration
REPORT_PATH = "reports/accessibility_report.html"
SCREENSHOT_PATH = "reports/screenshots/"