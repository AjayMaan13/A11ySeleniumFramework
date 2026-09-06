# Traceability matrix: WCAG criterion -> fixture page -> test function -> pass/fail.
# Formalizes the mapping that's already implicit in tests/test_accessibility.py's
# per-fixture assertions (missing_alt -> image-alt, contrast_issues -> color-contrast,
# form_labels -> label), and sources criterion descriptions from wcag_reference.py.

import os
import xml.etree.ElementTree as ET
from datetime import datetime

from src.utils.wcag_reference import get_wcag_explanation

# Fixture page -> WCAG criterion -> test function, based on the assertions
# actually made in tests/test_accessibility.py::test_local_site_accessibility.
TRACEABILITY_ENTRIES = [
    {
        "wcag_criterion": "1.1.1",
        "fixture_page": "missing_alt.html",
        "test_function": "test_local_site_accessibility",
    },
    {
        "wcag_criterion": "1.4.3",
        "fixture_page": "contrast_issues.html",
        "test_function": "test_local_site_accessibility",
    },
    {
        "wcag_criterion": "3.3.2",
        "fixture_page": "form_labels.html",
        "test_function": "test_local_site_accessibility",
    },
]


def parse_junit_results(junit_xml_path):
    """
    Parse a pytest --junitxml report into {node_id: 'pass'|'fail'|'skipped'}.

    Args:
        junit_xml_path: path to the junit XML file produced by pytest

    Returns:
        Dict mapping "classname::name" to status. Empty dict if the file
        doesn't exist or can't be parsed.
    """
    if not junit_xml_path or not os.path.exists(junit_xml_path):
        return {}

    try:
        tree = ET.parse(junit_xml_path)
    except ET.ParseError:
        return {}

    results = {}
    for testcase in tree.getroot().iter("testcase"):
        classname = testcase.get("classname", "")
        name = testcase.get("name", "")
        node_id = f"{classname}::{name}" if classname else name

        if testcase.find("failure") is not None or testcase.find("error") is not None:
            status = "fail"
        elif testcase.find("skipped") is not None:
            status = "skipped"
        else:
            status = "pass"

        results[node_id] = status

    return results


def _status_for(test_results, test_function, fixture_page):
    matches = [
        status
        for node_id, status in test_results.items()
        if test_function in node_id and fixture_page in node_id
    ]
    if not matches:
        return "not run"
    if "fail" in matches:
        return "fail"
    return "pass"


def generate_traceability_matrix(test_results):
    """
    Build the WCAG criterion -> fixture page -> test function -> status rows.

    Args:
        test_results: dict of node id -> status, as returned by
            parse_junit_results(). Pass {} if no run data is available;
            rows will report status 'not run'.

    Returns:
        List of dicts: {wcag_criterion, criterion_description, fixture_page,
        test_function, status}
    """
    test_results = test_results or {}

    rows = []
    for entry in TRACEABILITY_ENTRIES:
        rows.append(
            {
                "wcag_criterion": entry["wcag_criterion"],
                "criterion_description": get_wcag_explanation(entry["wcag_criterion"])
                or "No description available",
                "fixture_page": entry["fixture_page"],
                "test_function": entry["test_function"],
                "status": _status_for(
                    test_results, entry["test_function"], entry["fixture_page"]
                ),
            }
        )

    return rows


def render_traceability_report(matrix, output_file="reports/traceability_report.html"):
    """
    Render the traceability matrix as a standalone HTML report, styled to
    match the existing dashboard.py / report_utils.py reports.

    Args:
        matrix: list of row dicts from generate_traceability_matrix()
        output_file: path to write the HTML report to

    Returns:
        Path to the generated report
    """
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    status_classes = {"pass": "status-pass", "fail": "status-fail"}

    rows_html = ""
    for row in matrix:
        status = row["status"]
        status_class = status_classes.get(status, "status-unknown")
        rows_html += f"""
                    <tr>
                        <td>{row['wcag_criterion']}</td>
                        <td>{row['criterion_description']}</td>
                        <td>{row['fixture_page']}</td>
                        <td>{row['test_function']}</td>
                        <td class="{status_class}">{status}</td>
                    </tr>
        """

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WCAG Traceability Matrix</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            header {
                background-color: #f4f4f4;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1, h2 {
                color: #444;
            }
            .card {
                background: white;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f4f4f4;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .status-pass {
                color: #2e7d32;
                font-weight: bold;
            }
            .status-fail {
                color: #c62828;
                font-weight: bold;
            }
            .status-unknown {
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>WCAG Traceability Matrix</h1>
                <p>Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </header>

            <div class="card">
                <table>
                    <tr>
                        <th>WCAG Criterion</th>
                        <th>Description</th>
                        <th>Fixture Page</th>
                        <th>Test Function</th>
                        <th>Status</th>
                    </tr>
                    """ + rows_html + """
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(html)

    print(f"Traceability report generated at {output_file}")
    return output_file
