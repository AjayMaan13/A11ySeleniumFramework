# Wires the triage pipeline together: scan -> group -> prioritize -> decide -> ticket.
# run_triage() is the actual "agent": every step is a real branch (dedup skip,
# LLM ticket_worthy skip), not a single pass-through call.

import time

from src.agent.grouping import group_by_root_cause
from src.agent.prioritization import prioritize
from src.agent.ticket_dedup import fingerprint
from src.core.accessibility_scanner import AccessibilityScanner
from src.core.webdriver_manager import setup_driver, teardown_driver
from src.pages.base_page import BasePage
from src.utils.targets import TARGETS as DEFAULT_TARGETS
from src.utils.targets import WCAG_LEVEL_TAGS


def collect_violations(targets=None, browser="chrome", headless=True):
    """
    Scan each configured target page and return a flat list of raw
    axe-core violations, each tagged with the page_url it came from -
    the input shape group_by_root_cause() expects.

    Args:
        targets: list of {'url', 'expected_wcag_level'} dicts, e.g. from
            data/targets.json via src.utils.targets.TARGETS. Defaults to
            that list if not given.
        browser: browser to scan with ("chrome" or "firefox")
        headless: run the browser headless

    Returns:
        List of axe-core violation dicts, each with a 'page_url' key added.
    """
    targets = DEFAULT_TARGETS if targets is None else targets

    driver = setup_driver(browser, headless)
    violations = []
    try:
        for target in targets:
            url = target["url"]
            expected_level = target.get("expected_wcag_level", "AA")

            scanner = AccessibilityScanner(driver)
            page = BasePage(driver)
            page.open(url)
            time.sleep(1)
            scanner.inject_axe()

            results = scanner.run_custom_scan(
                options={
                    "runOnly": {
                        "type": "tag",
                        "values": WCAG_LEVEL_TAGS.get(expected_level, WCAG_LEVEL_TAGS["AA"]),
                    }
                }
            )

            for violation in scanner.get_violations(results):
                violation["page_url"] = url
                violations.append(violation)
    finally:
        teardown_driver(driver)

    return violations


def run_triage(violations: list, llm, dedup, ticketer) -> list:
    """
    Group, prioritize, and file tickets for the violations that warrant one.

    Args:
        violations: raw axe-core violations (see collect_violations)
        llm: an object with describe_group(group) -> {'summary', 'fix',
            'ticket_worthy'} (src.agent.llm_client.LLMClient)
        dedup: an object with already_filed(fp) -> bool and
            record(fp, issue_number) (src.agent.ticket_dedup.DedupStore)
        ticketer: an object with create(group, description) -> issue id
            (src.integrations.github_issues.GitHubIssueCreator)

    Returns:
        List of issue numbers filed on this run.
    """
    groups = prioritize(group_by_root_cause(violations))
    filed = []

    for group in groups:
        fp = fingerprint(group)
        if dedup.already_filed(fp):
            continue  # decision: skip, already tracked

        description = llm.describe_group(group)
        if not description["ticket_worthy"]:
            continue  # decision: not worth a ticket

        issue_number = ticketer.create(group, description)
        dedup.record(fp, issue_number)
        filed.append(issue_number)

    return filed
