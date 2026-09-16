# Tests for src/integrations/github_issues.py. The GitHub API is always
# mocked here - never files a real issue.

from unittest.mock import MagicMock, patch

from src.integrations.github_issues import GitHubIssueCreator

SAMPLE_GROUP = {
    "rule_id": "image-alt",
    "page_url": "file:///tests/sites/missing_alt.html",
    "impact": "critical",
    "wcag_criterion": "1.1.1",
    "count": 3,
    "sample_html": ['<img src="a.png">', '<img src="b.png">'],
    "screenshots": ["reports/screenshots/run1/image-alt_0.png"],
}

SAMPLE_DESCRIPTION = {
    "summary": "Images are missing alt text.",
    "fix": "Add descriptive alt attributes to each image.",
    "ticket_worthy": True,
}


@patch("src.integrations.github_issues.Github")
def test_create_returns_issue_number(mock_github_cls):
    mock_repo = MagicMock()
    mock_issue = MagicMock(number=42)
    mock_repo.create_issue.return_value = mock_issue
    mock_github_cls.return_value.get_repo.return_value = mock_repo

    creator = GitHubIssueCreator(token="test-token", repo_name="owner/repo")
    issue_number = creator.create(SAMPLE_GROUP, SAMPLE_DESCRIPTION)

    assert issue_number == 42
    mock_github_cls.return_value.get_repo.assert_called_once_with("owner/repo")


@patch("src.integrations.github_issues.Github")
def test_create_sets_title_body_and_labels(mock_github_cls):
    mock_repo = MagicMock()
    mock_repo.create_issue.return_value = MagicMock(number=1)
    mock_github_cls.return_value.get_repo.return_value = mock_repo

    creator = GitHubIssueCreator(token="test-token", repo_name="owner/repo")
    creator.create(SAMPLE_GROUP, SAMPLE_DESCRIPTION)

    _, kwargs = mock_repo.create_issue.call_args
    assert "image-alt" in kwargs["title"]
    assert "3 instances" in kwargs["title"]
    assert "critical" in kwargs["title"]
    assert kwargs["labels"] == ["accessibility", "critical"]
    assert SAMPLE_DESCRIPTION["summary"] in kwargs["body"]
    assert SAMPLE_DESCRIPTION["fix"] in kwargs["body"]
    assert "1.1.1" in kwargs["body"]
    assert 'src="a.png"' in kwargs["body"]
    assert "reports/screenshots/run1/image-alt_0.png" in kwargs["body"]


@patch("src.integrations.github_issues.Github")
def test_create_omits_impact_label_when_missing(mock_github_cls):
    mock_repo = MagicMock()
    mock_repo.create_issue.return_value = MagicMock(number=1)
    mock_github_cls.return_value.get_repo.return_value = mock_repo

    group = dict(SAMPLE_GROUP)
    del group["impact"]

    creator = GitHubIssueCreator(token="test-token", repo_name="owner/repo")
    creator.create(group, SAMPLE_DESCRIPTION)

    _, kwargs = mock_repo.create_issue.call_args
    assert kwargs["labels"] == ["accessibility"]
