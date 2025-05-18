# CLI tool to run accessibility tests with various options

import argparse
import os
import sys
import pytest
from src.utils.dashboard import create_dashboard


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
    
    # Parse arguments
    args = parser.parse_args()
    
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
    
    # Prepare pytest arguments
    pytest_args = ["-v"]
    
    # Add HTML report
    report_path = os.path.join(args.output, "report.html")
    pytest_args.extend(["--html", report_path])
    
    # Run tests
    print(f"Running accessibility tests...")
    result = pytest.main(pytest_args)
    
    # Generate dashboard if requested
    if args.dashboard or True:  # Always generate dashboard for now
        print("Generating dashboard...")
        dashboard_path = create_dashboard(args.output)
        print(f"Dashboard available at: {dashboard_path}")
    
    # Return exit code
    return result


if __name__ == "__main__":
    sys.exit(main())