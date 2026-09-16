# Collapse per-page axe-core violations into one group per (rule, page),
# so N node-level hits of the same rule become a single ticket-shaped
# unit instead of N. Pure logic: no browser, no API calls, just dicts in
# and dicts out - see tests/test_grouping.py.


def group_by_root_cause(violations: list) -> list:
    """
    Args:
        violations: raw axe-core violation dicts, as returned by
            AccessibilityScanner.get_violations(), each optionally
            carrying a 'page_url' key (axe itself doesn't know which
            page it scanned - the caller attaches this) and a
            'wcag_criterion' key. Individual nodes may carry a
            'screenshot_path' key, set by AccessibilityScanner (Phase 0b).

    Returns:
        One group dict per (rule_id, page_url), each with: rule_id,
        page_url, impact, wcag_criterion, count, sample_html (up to 3
        node HTML snippets), screenshots (node screenshot paths, where
        present). 12 'image-alt' hits on a page become 1 group with
        count=12, not 12 tickets.
    """
    groups = {}
    for violation in violations:
        key = (violation["id"], violation.get("page_url"))
        if key not in groups:
            groups[key] = {
                "rule_id": violation["id"],
                "page_url": violation.get("page_url"),
                "impact": violation.get("impact"),
                "wcag_criterion": violation.get("wcag_criterion"),
                "count": 0,
                "sample_html": [],
                "screenshots": [],
            }

        group = groups[key]
        for node in violation.get("nodes", []):
            group["count"] += 1
            if len(group["sample_html"]) < 3:
                group["sample_html"].append(node.get("html", ""))
            if node.get("screenshot_path"):
                group["screenshots"].append(node["screenshot_path"])

    return list(groups.values())
