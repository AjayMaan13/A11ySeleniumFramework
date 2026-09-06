# Tests for the AI remediation module. The Anthropic API is always mocked here.

import json
import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.core.ai_analyzer import get_ai_remediation

SAMPLE_VIOLATIONS = [
    {
        "id": "image-alt",
        "help": "Images must have alternate text",
        "impact": "critical",
        "tags": ["wcag2a", "wcag111"],
        "nodes": [{"html": "<img src=\"x.png\">"}],
    },
    {
        "id": "color-contrast",
        "help": "Elements must have sufficient color contrast",
        "impact": "serious",
        "tags": ["wcag2aa", "wcag143"],
        "nodes": [{"html": "<p class=\"low-contrast-1\">low contrast text</p>"}],
    },
]


def _mock_response(payload):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps(payload))])


@patch("anthropic.Anthropic")
def test_get_ai_remediation_adds_suggestion_on_valid_response(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(
        [
            {"index": 0, "fix": "Add descriptive alt text to the image.", "priority": "high"},
            {"index": 1, "fix": "Darken the text color to meet 4.5:1 contrast.", "priority": "medium"},
        ]
    )
    mock_anthropic_cls.return_value = mock_client

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
        result = get_ai_remediation(SAMPLE_VIOLATIONS)

    assert result[0]["ai_suggestion"] == {
        "fix": "Add descriptive alt text to the image.",
        "priority": "high",
    }
    assert result[1]["ai_suggestion"] == {
        "fix": "Darken the text color to meet 4.5:1 contrast.",
        "priority": "medium",
    }
    # Original violation fields must be preserved untouched.
    assert result[0]["id"] == "image-alt"
    assert result[1]["id"] == "color-contrast"
    # One batched call, not one call per violation.
    mock_client.messages.create.assert_called_once()


@patch("anthropic.Anthropic")
def test_get_ai_remediation_fails_gracefully_on_api_error(mock_anthropic_cls):
    mock_anthropic_cls.side_effect = RuntimeError("API unavailable")

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
        result = get_ai_remediation(SAMPLE_VIOLATIONS)

    assert result == [dict(v, ai_suggestion=None) for v in SAMPLE_VIOLATIONS]


def test_get_ai_remediation_without_api_key_returns_originals(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    result = get_ai_remediation(SAMPLE_VIOLATIONS)

    assert result == [dict(v, ai_suggestion=None) for v in SAMPLE_VIOLATIONS]


def test_get_ai_remediation_empty_input_returns_empty():
    assert get_ai_remediation([]) == []
