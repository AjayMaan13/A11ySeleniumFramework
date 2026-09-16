# Files GitHub Issues for ticket-worthy accessibility violation groups.

from github import Github


class GitHubIssueCreator:
    def __init__(self, token: str, repo_name: str):
        self.repo = Github(token).get_repo(repo_name)

    def create(self, group: dict, ai_description: dict) -> int:
        """
        File a GitHub issue for one violation group.

        Args:
            group: a group dict from src.agent.grouping.group_by_root_cause
            ai_description: the dict from LLMClient.describe_group
                ({'summary', 'fix', 'ticket_worthy'})

        Returns:
            The number of the created issue.
        """
        title = (
            f"[A11y] {group['rule_id']} - {group['count']} instances "
            f"({group.get('impact', 'unknown')})"
        )
        body = self._build_body(group, ai_description)

        labels = ["accessibility"]
        if group.get("impact"):
            labels.append(group["impact"])

        issue = self.repo.create_issue(title=title, body=body, labels=labels)
        return issue.number

    def _build_body(self, group: dict, ai_description: dict) -> str:
        sample_html = "\n".join(group.get("sample_html", []))

        body = f"""## {ai_description['summary']}

**WCAG criterion:** {group.get('wcag_criterion', 'N/A')}
**Impact:** {group.get('impact', 'unknown')}
**Instances found:** {group['count']}
**Page:** {group.get('page_url', 'N/A')}

### Suggested fix
{ai_description['fix']}

### Sample affected elements
```html
{sample_html}
```
"""

        screenshots = group.get("screenshots") or []
        if screenshots:
            # These are local filesystem paths from the test run, not
            # uploaded images - GitHub's Issues API has no direct image
            # upload endpoint, so linking would need the screenshots
            # committed to the repo first. Noting the paths keeps them
            # discoverable without inventing an upload step that isn't
            # actually wired up.
            body += "\n### Screenshots (from the test run)\n"
            body += "\n".join(f"- `{path}`" for path in screenshots)

        return body
