# Tests for the triage orchestration logic in src/agent/triage.py.
# llm, dedup, and ticketer are all mocked - run_triage() takes them as
# injected dependencies precisely so this can be tested without hitting
# a real LLM or GitHub API, or costing tokens on every CI run.

from unittest.mock import MagicMock

from src.agent.triage import run_triage


def _violation(rule_id, page_url, impact, node_count=1):
    return {
        "id": rule_id,
        "page_url": page_url,
        "impact": impact,
        "nodes": [{"html": f"<div id='{i}'>"} for i in range(node_count)],
    }


def _make_llm(ticket_worthy=True):
    llm = MagicMock()
    llm.describe_group.return_value = {
        "summary": "summary",
        "fix": "fix",
        "ticket_worthy": ticket_worthy,
    }
    return llm


def test_files_ticket_for_new_ticket_worthy_group():
    violations = [_violation("image-alt", "page-a.html", "critical")]
    llm = _make_llm(ticket_worthy=True)
    dedup = MagicMock()
    dedup.already_filed.return_value = False
    ticketer = MagicMock()
    ticketer.create.return_value = 101

    filed = run_triage(violations, llm, dedup, ticketer)

    assert filed == [101]
    ticketer.create.assert_called_once()
    dedup.record.assert_called_once()


def test_skips_group_already_filed():
    violations = [_violation("image-alt", "page-a.html", "critical")]
    llm = _make_llm(ticket_worthy=True)
    dedup = MagicMock()
    dedup.already_filed.return_value = True
    ticketer = MagicMock()

    filed = run_triage(violations, llm, dedup, ticketer)

    assert filed == []
    llm.describe_group.assert_not_called()
    ticketer.create.assert_not_called()
    dedup.record.assert_not_called()


def test_skips_group_llm_marks_not_ticket_worthy():
    violations = [_violation("region", "page-a.html", "minor")]
    llm = _make_llm(ticket_worthy=False)
    dedup = MagicMock()
    dedup.already_filed.return_value = False
    ticketer = MagicMock()

    filed = run_triage(violations, llm, dedup, ticketer)

    assert filed == []
    ticketer.create.assert_not_called()
    dedup.record.assert_not_called()


def test_call_order_is_dedup_then_llm_then_ticket_then_record():
    violations = [_violation("image-alt", "page-a.html", "critical")]
    call_order = []

    dedup = MagicMock()
    dedup.already_filed.side_effect = lambda fp: call_order.append("already_filed") or False
    dedup.record.side_effect = lambda fp, n: call_order.append("record")

    llm = MagicMock()
    llm.describe_group.side_effect = lambda g: call_order.append("describe_group") or {
        "summary": "s",
        "fix": "f",
        "ticket_worthy": True,
    }

    ticketer = MagicMock()
    ticketer.create.side_effect = lambda g, d: call_order.append("create") or 55

    run_triage(violations, llm, dedup, ticketer)

    assert call_order == ["already_filed", "describe_group", "create", "record"]


def test_processes_multiple_groups_and_files_higher_priority_first():
    violations = [
        _violation("region", "page-a.html", "minor"),
        _violation("image-alt", "page-a.html", "critical"),
    ]
    llm = _make_llm(ticket_worthy=True)
    dedup = MagicMock()
    dedup.already_filed.return_value = False
    ticketer = MagicMock()
    ticketer.create.side_effect = [201, 202]

    filed = run_triage(violations, llm, dedup, ticketer)

    # critical (image-alt) is prioritized ahead of minor (region)
    first_group_arg = ticketer.create.call_args_list[0].args[0]
    assert first_group_arg["rule_id"] == "image-alt"
    assert filed == [201, 202]


def test_mixed_skip_and_file_across_groups():
    violations = [
        _violation("image-alt", "page-a.html", "critical"),
        _violation("region", "page-a.html", "minor"),
    ]
    dedup = MagicMock()
    dedup.already_filed.return_value = False
    ticketer = MagicMock()
    ticketer.create.return_value = 301

    llm = MagicMock()
    llm.describe_group.side_effect = [
        {"summary": "s", "fix": "f", "ticket_worthy": True},  # image-alt: file it
        {"summary": "s", "fix": "f", "ticket_worthy": False},  # region: skip it
    ]

    filed = run_triage(violations, llm, dedup, ticketer)

    assert filed == [301]
    ticketer.create.assert_called_once()
    dedup.record.assert_called_once()
