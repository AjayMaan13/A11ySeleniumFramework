# Loads the data-driven scan target list (data/targets.json). Lives in src/
# rather than tests/ since both the test suite and the triage agent's scan
# step (src/agent/triage.py) need it - a new page to test/triage is a new
# row in the JSON file, not a code change in either place.

import json
import os
from urllib.request import pathname2url

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_TARGETS_PATH = os.path.join(_PROJECT_ROOT, "data", "targets.json")

# WCAG level -> axe-core tags a target's expected_wcag_level maps to
WCAG_LEVEL_TAGS = {
    "A": ["wcag2a"],
    "AA": ["wcag2a", "wcag2aa"],
    "AAA": ["wcag2a", "wcag2aa", "wcag2aaa"],
}


def load_targets(targets_path=_TARGETS_PATH):
    """
    Load data/targets.json and resolve local (non-http) target paths to
    absolute file:// URLs, so callers work regardless of the current
    working directory.
    """
    with open(targets_path) as targets_file:
        targets = json.load(targets_file)

    for target in targets:
        if not target["url"].startswith(("http://", "https://", "file://")):
            abs_path = os.path.join(_PROJECT_ROOT, target["url"])
            target["url"] = "file:" + pathname2url(abs_path)

    return targets


TARGETS = load_targets()
