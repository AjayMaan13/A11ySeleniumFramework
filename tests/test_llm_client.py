# Tests for the triage agent's LLM client. The Anthropic API is always mocked here.

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.agent.llm_client import LLMClient

SAMPLE_GROUP = {
    "rule_id": "image-alt",
    "page_url": "file:///tests/sites/missing_alt.html",
    "impact": "critical",
    "count": 3,
    "sample_html": ['<img src="a.png">', '<img src="b.png">'],
}


def _mock_response(text):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


@patch("src.agent.llm_client.anthropic.Anthropic")
def test_describe_group_parses_valid_json(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(
        json.dumps(
            {
                "summary": "Images are missing alt text.",
                "fix": "Add descriptive alt attributes to each image.",
                "ticket_worthy": True,
            }
        )
    )
    mock_anthropic_cls.return_value = mock_client

    client = LLMClient(api_key="test-key")
    result = client.describe_group(SAMPLE_GROUP)

    assert result == {
        "summary": "Images are missing alt text.",
        "fix": "Add descriptive alt attributes to each image.",
        "ticket_worthy": True,
    }
    mock_client.messages.create.assert_called_once()


@patch("src.agent.llm_client.anthropic.Anthropic")
def test_describe_group_extracts_json_embedded_in_prose(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(
        'Sure, here you go:\n{"summary": "s", "fix": "f", "ticket_worthy": false}\nHope that helps!'
    )
    mock_anthropic_cls.return_value = mock_client

    client = LLMClient(api_key="test-key")
    result = client.describe_group(SAMPLE_GROUP)

    assert result == {"summary": "s", "fix": "f", "ticket_worthy": False}


@patch("src.agent.llm_client.anthropic.Anthropic")
def test_describe_group_fails_open_on_malformed_response(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response("not json at all")
    mock_anthropic_cls.return_value = mock_client

    client = LLMClient(api_key="test-key")
    result = client.describe_group(SAMPLE_GROUP)

    assert result["ticket_worthy"] is True
    assert "image-alt" in result["summary"]


@patch("src.agent.llm_client.anthropic.Anthropic")
def test_describe_group_fails_open_on_missing_fields(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(
        json.dumps({"summary": "s"})
    )
    mock_anthropic_cls.return_value = mock_client

    client = LLMClient(api_key="test-key")
    result = client.describe_group(SAMPLE_GROUP)

    assert result["ticket_worthy"] is True
