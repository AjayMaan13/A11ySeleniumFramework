# AI-driven remediation guidance for axe-core violations.
# Additive only: never changes what the scanner detects, only annotates results.

import json
import logging
import os
import re

logger = logging.getLogger(__name__)

# Overridable so callers can trade cost/quality without a code change.
DEFAULT_MODEL = os.environ.get("ANTHROPIC_AI_ANALYZER_MODEL", "claude-3-5-haiku-latest")

VALID_PRIORITIES = {"high", "medium", "low"}


def get_ai_remediation(violations):
    """
    Enrich axe-core violations with AI-generated remediation guidance.

    Args:
        violations: list of violation dicts as produced by
            AccessibilityScanner.get_violations()

    Returns:
        A new list of violations, each with an added 'ai_suggestion' key.
        The value is {'fix': str, 'priority': 'high'|'medium'|'low'} on
        success, or None if the API key is missing or the request fails.
    """
    if not violations:
        return violations

    enriched = [dict(violation, ai_suggestion=None) for violation in violations]

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning(
            "ANTHROPIC_API_KEY not set; skipping AI remediation suggestions"
        )
        return enriched

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": _build_prompt(violations)}],
        )
        suggestions = _parse_response(response, len(violations))
    except Exception as exc:
        logger.warning(
            "AI remediation request failed, continuing without suggestions: %s", exc
        )
        return enriched

    for violation, suggestion in zip(enriched, suggestions):
        violation["ai_suggestion"] = suggestion

    return enriched


def _extract_wcag_tags(violation):
    """Pull the axe-core WCAG tags (e.g. 'wcag111') off a violation, as-is."""
    return [tag for tag in violation.get("tags", []) if re.match(r"^wcag\d", tag)]


def _build_prompt(violations):
    items = []
    for index, violation in enumerate(violations):
        nodes = violation.get("nodes") or []
        items.append(
            {
                "index": index,
                "wcag_tags": _extract_wcag_tags(violation),
                "description": violation.get("help", ""),
                "html_snippet": nodes[0].get("html", "") if nodes else "",
            }
        )

    return (
        "You are a web accessibility expert. For each violation in the JSON "
        "array below, provide a one-sentence plain-English fix and a "
        'priority ("high", "medium", or "low").\n'
        "Respond with ONLY a JSON array of objects shaped like "
        '{"index": <int>, "fix": "<string>", "priority": "high|medium|low"}, '
        "one per violation, with no other text.\n\n"
        f"Violations:\n{json.dumps(items, indent=2)}"
    )


def _parse_response(response, expected_count):
    text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            raise
        data = json.loads(match.group(0))

    suggestions = [None] * expected_count
    for item in data:
        index = item.get("index")
        fix = item.get("fix")
        priority = item.get("priority")
        if (
            isinstance(index, int)
            and 0 <= index < expected_count
            and fix
            and priority in VALID_PRIORITIES
        ):
            suggestions[index] = {"fix": fix, "priority": priority}

    return suggestions
