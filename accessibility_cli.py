# CLI tool to run accessibility tests with various options

import argparse
import os
import sys
import pytest
from src.utils.dashboard import create_dashboard


def run_triage_cli(args):
    """
    Scan the configured targets and file GitHub issues for ticket-worthy
    violation groups. Separate from the pytest-based flow in main() since
    it drives its own scan rather than asserting pass/fail on test pages.

    Returns:
        0 on success, 1 if a required credential/argument is missing.
    """
    github_token = os.environ.get("GITHUB_TOKEN")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if not args.repo:
        print("Error: --triage requires --repo owner/name")
        return 1
    if not github_token:
        print("Error: --triage requires a GITHUB_TOKEN environment variable")
        return 1
    if not anthropic_key:
        print("Error: --triage requires an ANTHROPIC_API_KEY environment variable")
        return 1

    from src.agent.llm_client import LLMClient
    from src.agent.ticket_dedup import DedupStore
    from src.agent.triage import collect_violations, run_triage
    from src.integrations.github_issues import GitHubIssueCreator

    print("Scanning configured targets (data/targets.json)...")
    violations = collect_violations(browser=args.browser, headless=args.headless)
    print(f"Found {len(violations)} raw violations across targets.")

    llm = LLMClient(api_key=anthropic_key)
    dedup = DedupStore()
    ticketer = GitHubIssueCreator(token=github_token, repo_name=args.repo)

    filed = run_triage(violations, llm, dedup, ticketer)

    if filed:
        print(f"Filed {len(filed)} new issue(s) on {args.repo}: {filed}")
    else:
        print("No new tickets filed (nothing ticket-worthy, or already tracked).")

    return 0


def main():
    """
    Command line interface for running accessibility tests
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Accessibility Testing Framework CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Add arguments
    parser.add_argument(
        "--url", "-u",
        help="URL to test for accessibility issues",
        default=None
    )
    
    parser.add_argument(
        "--browser", "-b",
        help="Browser to use for testing",
        choices=["chrome", "firefox"],
        default="chrome"
    )
    
    parser.add_argument(
        "--headless",
        help="Run browser in headless mode",
        action="store_true"
    )
    
    parser.add_argument(
        "--wcag", "-w",
        help="WCAG level to test",
        choices=["A", "AA", "AAA"],
        default="AA"
    )
    
    parser.add_argument(
        "--rules", "-r",
        help="Specific rules to test (comma-separated)",
        default=None
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output directory for reports",
        default="reports"
    )
    
    parser.add_argument(
        "--dashboard",
        help="Generate dashboard after tests",
        action="store_true"
    )

    parser.add_argument(
        "--ai-suggestions",
        help="Use the Anthropic API to add plain-English remediation suggestions to violations (requires ANTHROPIC_API_KEY)",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--traceability",
        help="Generate a WCAG criterion -> fixture page -> test function traceability report after the run",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--triage",
        help="Scan the configured targets (data/targets.json), group and prioritize "
             "violations, and file a GitHub issue for each ticket-worthy group "
             "(requires GITHUB_TOKEN and ANTHROPIC_API_KEY env vars, and --repo). "
             "Runs instead of the pytest suite.",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--repo",
        help="GitHub repo to file --triage tickets against, as owner/name",
        default=None
    )

    # Parse arguments
    args = parser.parse_args()

    if args.triage:
        return run_triage_cli(args)
    
    # Update configuration based on arguments
    if args.url:
        # Set environment variable for test_accessibility.py to use
        os.environ["TEST_URL"] = args.url
    
    if args.browser:
        os.environ["TEST_BROWSER"] = args.browser
    
    if args.headless:
        os.environ["TEST_HEADLESS"] = "1"
    
    if args.wcag:
        os.environ["TEST_WCAG_LEVEL"] = args.wcag
    
    if args.rules:
        os.environ["TEST_RULES"] = args.rules
    
    if args.output:
        os.environ["TEST_OUTPUT"] = args.output

    if args.ai_suggestions:
        os.environ["TEST_AI_SUGGESTIONS"] = "1"

    # Prepare pytest arguments
    pytest_args = ["-v"]

    # Add HTML report
    report_path = os.path.join(args.output, "report.html")
    pytest_args.extend(["--html", report_path])

    # Traceability needs per-test pass/fail status, which pytest's built-in
    # junitxml output gives us without adding a new dependency.
    junit_path = os.path.join(args.output, "junit.xml")
    if args.traceability:
        pytest_args.extend(["--junitxml", junit_path])

    # Run tests
    print(f"Running accessibility tests...")
    result = pytest.main(pytest_args)

    # Generate dashboard if requested
    if args.dashboard or True:  # Always generate dashboard for now
        print("Generating dashboard...")
        dashboard_path = create_dashboard(args.output)
        print(f"Dashboard available at: {dashboard_path}")

    if args.traceability:
        from src.utils.traceability import (
            generate_traceability_matrix,
            parse_junit_results,
            render_traceability_report,
        )

        print("Generating traceability matrix...")
        test_results = parse_junit_results(junit_path)
        matrix = generate_traceability_matrix(test_results)
        traceability_path = os.path.join(args.output, "traceability_report.html")
        render_traceability_report(matrix, traceability_path)
        print(f"Traceability report available at: {traceability_path}")

    # Return exit code
    return result


if __name__ == "__main__":
    sys.exit(main())