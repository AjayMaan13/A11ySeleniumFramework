# Tests for src/agent/prioritization.py. Pure logic, dicts in and dicts out.

from src.agent.prioritization import prioritize


def _group(rule_id, impact, count):
    return {"rule_id": rule_id, "impact": impact, "count": count}


def test_sorts_by_impact_severity():
    groups = [
        _group("minor-rule", "minor", 1),
        _group("critical-rule", "critical", 1),
        _group("moderate-rule", "moderate", 1),
        _group("serious-rule", "serious", 1),
    ]

    result = prioritize(groups)

    assert [g["rule_id"] for g in result] == [
        "critical-rule",
        "serious-rule",
        "moderate-rule",
        "minor-rule",
    ]


def test_breaks_impact_ties_by_instance_count_descending():
    groups = [
        _group("rule-a", "serious", 2),
        _group("rule-b", "serious", 10),
        _group("rule-c", "serious", 5),
    ]

    result = prioritize(groups)

    assert [g["rule_id"] for g in result] == ["rule-b", "rule-c", "rule-a"]


def test_unknown_impact_sorts_last_but_is_not_dropped():
    groups = [
        _group("rule-a", "critical", 1),
        _group("rule-b", "weird-impact", 100),
    ]

    result = prioritize(groups)

    assert len(result) == 2
    assert result[-1]["rule_id"] == "rule-b"


def test_missing_impact_and_count_do_not_raise():
    groups = [{"rule_id": "rule-a"}, _group("rule-b", "critical", 1)]

    result = prioritize(groups)

    assert [g["rule_id"] for g in result] == ["rule-b", "rule-a"]


def test_empty_input_returns_empty_list():
    assert prioritize([]) == []
