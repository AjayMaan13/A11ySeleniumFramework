# Tests for src/agent/grouping.py. Pure logic, no browser or API involved -
# hand-crafted axe-core-shaped violation fixtures only.

from src.agent.grouping import group_by_root_cause


def _violation(rule_id, page_url, impact, node_htmls, wcag_criterion=None, screenshots=None):
    screenshots = screenshots or [None] * len(node_htmls)
    return {
        "id": rule_id,
        "page_url": page_url,
        "impact": impact,
        "wcag_criterion": wcag_criterion,
        "nodes": [
            {"html": html, **({"screenshot_path": shot} if shot else {})}
            for html, shot in zip(node_htmls, screenshots)
        ],
    }


def test_collapses_multiple_nodes_of_same_rule_and_page_into_one_group():
    violations = [
        _violation(
            "image-alt",
            "file:///missing_alt.html",
            "critical",
            ["<img>", "<img class='b'>", "<img class='c'>"],
        )
    ]

    groups = group_by_root_cause(violations)

    assert len(groups) == 1
    assert groups[0]["rule_id"] == "image-alt"
    assert groups[0]["page_url"] == "file:///missing_alt.html"
    assert groups[0]["impact"] == "critical"
    assert groups[0]["count"] == 3


def test_same_rule_on_different_pages_stays_separate():
    violations = [
        _violation("image-alt", "page-a.html", "critical", ["<img>"]),
        _violation("image-alt", "page-b.html", "critical", ["<img>"]),
    ]

    groups = group_by_root_cause(violations)

    assert len(groups) == 2
    assert {g["page_url"] for g in groups} == {"page-a.html", "page-b.html"}


def test_different_rules_on_same_page_stay_separate():
    violations = [
        _violation("image-alt", "page-a.html", "critical", ["<img>"]),
        _violation("color-contrast", "page-a.html", "serious", ["<p>"]),
    ]

    groups = group_by_root_cause(violations)

    assert len(groups) == 2
    assert {g["rule_id"] for g in groups} == {"image-alt", "color-contrast"}


def test_two_violation_entries_for_same_rule_and_page_merge_counts():
    # e.g. axe returning the same rule twice across a multi-context scan
    violations = [
        _violation("label", "page-a.html", "serious", ["<input>"]),
        _violation("label", "page-a.html", "serious", ["<select>", "<textarea>"]),
    ]

    groups = group_by_root_cause(violations)

    assert len(groups) == 1
    assert groups[0]["count"] == 3


def test_sample_html_capped_at_three():
    violations = [
        _violation(
            "image-alt",
            "page-a.html",
            "critical",
            ["<img1>", "<img2>", "<img3>", "<img4>", "<img5>"],
        )
    ]

    groups = group_by_root_cause(violations)

    assert groups[0]["count"] == 5
    assert groups[0]["sample_html"] == ["<img1>", "<img2>", "<img3>"]


def test_screenshots_collected_only_when_present():
    violations = [
        _violation(
            "image-alt",
            "page-a.html",
            "critical",
            ["<img1>", "<img2>"],
            screenshots=["reports/screenshots/run1/image-alt_0.png", None],
        )
    ]

    groups = group_by_root_cause(violations)

    assert groups[0]["screenshots"] == ["reports/screenshots/run1/image-alt_0.png"]


def test_wcag_criterion_passed_through():
    violations = [
        _violation("image-alt", "page-a.html", "critical", ["<img>"], wcag_criterion="1.1.1")
    ]

    groups = group_by_root_cause(violations)

    assert groups[0]["wcag_criterion"] == "1.1.1"


def test_empty_input_returns_empty_list():
    assert group_by_root_cause([]) == []
