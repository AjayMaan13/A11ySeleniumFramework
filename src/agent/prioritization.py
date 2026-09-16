# Order grouped violations so the most urgent, widest-reaching issues surface
# first. Pure logic: no browser, no API calls, just dicts in and dicts out.

IMPACT_RANK = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}


def prioritize(groups: list) -> list:
    """Sort by axe-core's own impact ranking, then by breadth (instance count).

    Unrecognized or missing impact values sort last rather than raising,
    since a malformed group is still worth surfacing.
    """
    return sorted(groups, key=lambda g: (IMPACT_RANK.get(g.get("impact"), len(IMPACT_RANK)), -g.get("count", 0)))
