# LLM client for the triage agent's group-level analysis (Phase 2+).
#
# --ai-suggestions already has its own complete implementation in
# src/core/ai_analyzer.py: one batched API call per scan that annotates
# each violation with a plain-English fix. That's a different shape of
# request (per-violation, single call for the whole scan) than what the
# triage pipeline needs (per-group, plus a keep/skip judgment), so this
# client is additive rather than a replacement.

import json
import logging
import os
import re

import anthropic

logger = logging.getLogger(__name__)

# Overridable so callers can trade cost/quality without a code change,
# consistent with src/core/ai_analyzer.py's DEFAULT_MODEL pattern.
DEFAULT_MODEL = os.environ.get("ANTHROPIC_AGENT_MODEL", "claude-3-5-haiku-latest")


class LLMClient:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def describe_group(self, group: dict) -> dict:
        """
        Get a root-cause summary, concrete fix, and file/skip judgment for
        one group of same-rule violations (see src/agent/grouping.py).

        Returns a dict with 'summary', 'fix', and 'ticket_worthy' keys.
        Fails open (ticket_worthy=True) on a malformed or unparseable
        response, so a real accessibility issue never gets silently
        dropped just because the model's JSON was messy.
        """
        prompt = _build_group_prompt(group)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_group_response(response, group)


def _build_group_prompt(group: dict) -> str:
    return (
        f"{group.get('count', 1)} instances of WCAG violation "
        f"'{group.get('rule_id', 'unknown')}' found across this page "
        f"(impact: {group.get('impact', 'unknown')}).\n"
        f"Sample affected elements: {json.dumps(group.get('sample_html', [])[:3])}\n\n"
        "Return JSON with exactly these keys:\n"
        '- "summary": one-sentence root-cause description\n'
        '- "fix": concrete fix a developer should make\n'
        '- "ticket_worthy": true/false - false only for trivial, '
        "single-instance, minor-impact issues\n"
        "Respond with ONLY the JSON object, no other text."
    )


def _parse_group_response(response, group: dict) -> dict:
    text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    data = None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                data = None

    if isinstance(data, dict):
        summary, fix, ticket_worthy = (
            data.get("summary"),
            data.get("fix"),
            data.get("ticket_worthy"),
        )
        if summary and fix and isinstance(ticket_worthy, bool):
            return {"summary": summary, "fix": fix, "ticket_worthy": ticket_worthy}

    logger.warning(
        "Could not parse LLM group description, filing a ticket to be safe: %r",
        text[:200],
    )
    return _fallback_description(group)


def _fallback_description(group: dict) -> dict:
    return {
        "summary": (
            f"{group.get('count', 1)} instance(s) of "
            f"'{group.get('rule_id', 'unknown')}' "
            f"({group.get('impact', 'unknown')} impact)."
        ),
        "fix": "See the axe-core rule documentation for this violation.",
        "ticket_worthy": True,
    }
