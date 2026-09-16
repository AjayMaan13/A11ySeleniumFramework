# Test configuration file

import json
import os
from urllib.request import pathname2url

# Data-driven local targets: add a row to data/targets.json to test a new
# page, no code changes needed (mirrors an Input Data Sheet pattern).
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TARGETS_PATH = os.path.join(_PROJECT_ROOT, "data", "targets.json")

with open(_TARGETS_PATH) as _targets_file:
    TARGETS = json.load(_targets_file)

# Resolve local (non-http) target paths to absolute file:// URLs so tests
# work regardless of the current working directory.
for _target in TARGETS:
    if not _target["url"].startswith(("http://", "https://", "file://")):
        _abs_path = os.path.join(_PROJECT_ROOT, _target["url"])
        _target["url"] = "file:" + pathname2url(_abs_path)

# WCAG level -> axe-core tags a target's expected_wcag_level maps to
WCAG_LEVEL_TAGS = {
    "A": ["wcag2a"],
    "AA": ["wcag2a", "wcag2aa"],
    "AAA": ["wcag2a", "wcag2aa", "wcag2aaa"],
}

# URLs to test - a mix of public sites and local files
TEST_URLS = {
    # Public sites known to have some accessibility issues
    "public": [
        "https://www.example.com",  # Simple site for testing
        "https://www.w3.org/WAI/demos/bad/",  # W3C's "Before and After" demo site
        "https://dequeuniversity.com/demo/mars/"  # Deque's Mars Commuter demo site
    ],

    # Local test files - sourced from data/targets.json
    "local": [t["url"] for t in TARGETS]
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