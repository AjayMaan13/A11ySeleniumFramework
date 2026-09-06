# Step definitions for tests/features/accessibility.feature.
# Thin wrappers only - all scanning logic lives in src/core/accessibility_scanner.py.

import os
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.core.accessibility_scanner import AccessibilityScanner
from src.core.webdriver_manager import setup_driver, teardown_driver
from src.pages.base_page import BasePage

scenarios("accessibility.feature")

SITES_DIR = Path(__file__).resolve().parent.parent / "sites"

# The WCAG criterion each fixture page is known to violate, per the
# assertions already made in tests/test_accessibility.py.
WCAG_TO_AXE_RULE = {
    "1.1.1": "image-alt",
    "1.4.3": "color-contrast",
    "3.3.2": "label",
}


@pytest.fixture
def bdd_driver():
    """WebDriver for the BDD scenarios, independent of the pytest suite's own `driver` fixture."""
    browser = os.environ.get("TEST_BROWSER", "chrome")
    headless = os.environ.get("TEST_HEADLESS", "0") == "1"
    driver = setup_driver(browser, headless)
    driver.set_window_size(1366, 768)
    yield driver
    teardown_driver(driver)


@pytest.fixture
def scan_context():
    return {}


def _open_fixture_page(driver, filename, scan_context):
    page_path = SITES_DIR / filename
    page = BasePage(driver)
    page.open(f"file://{page_path.resolve()}")
    scan_context["driver"] = driver
    return scan_context


@given("a page with missing alt text", target_fixture="scan_context")
def given_missing_alt_page(bdd_driver, scan_context):
    return _open_fixture_page(bdd_driver, "missing_alt.html", scan_context)


@given("a page with insufficient color contrast", target_fixture="scan_context")
def given_contrast_issues_page(bdd_driver, scan_context):
    return _open_fixture_page(bdd_driver, "contrast_issues.html", scan_context)


@given("a page with unlabeled form fields", target_fixture="scan_context")
def given_form_labels_page(bdd_driver, scan_context):
    return _open_fixture_page(bdd_driver, "form_labels.html", scan_context)


@when("the accessibility scanner runs")
def run_accessibility_scanner(scan_context):
    scanner = AccessibilityScanner(scan_context["driver"])
    scanner.inject_axe()
    results = scanner.run_full_scan()
    scan_context["violations"] = scanner.get_violations(results)


@then(parsers.parse("a WCAG {criterion} violation is reported"))
def assert_wcag_violation_reported(criterion, scan_context):
    axe_rule = WCAG_TO_AXE_RULE.get(criterion)
    assert axe_rule, f"No axe-core rule mapped for WCAG {criterion}"

    matching = [v for v in scan_context["violations"] if v.get("id") == axe_rule]
    assert matching, f"Expected a '{axe_rule}' violation for WCAG {criterion}, found none"
