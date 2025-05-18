# Utility for creating an enhanced HTML dashboard of test results

import os
import glob
import json
from datetime import datetime
from pathlib import Path


def create_dashboard(report_dir="reports", output_file="reports/dashboard.html"):
    """
    Create a dashboard HTML file that links to all generated reports
    
    Args:
        report_dir: Directory containing reports
        output_file: Path for the dashboard HTML file
    
    Returns:
        Path to the generated dashboard
    """
    # Make sure the reports directory exists
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # Find all HTML reports
    report_files = glob.glob(os.path.join(report_dir, "accessibility_*.html"))
    rule_reports = glob.glob(os.path.join(report_dir, "rule_*.html"))
    
    # Find all screenshots
    screenshots = glob.glob(os.path.join(report_dir, "screenshots", "*.png"))
    
    # Create dashboard HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Accessibility Testing Dashboard</title>
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
            h1, h2, h3 {
                color: #444;
            }
            .card {
                background: white;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .summary {
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
            }
            .summary-card {
                flex: 1;
                min-width: 200px;
                margin: 10px;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
            }
            .summary-value {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
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
            a {
                color: #0066cc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .screenshot-gallery {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .screenshot-card {
                flex: 1;
                min-width: 250px;
                max-width: 300px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-radius: 5px;
                overflow: hidden;
            }
            .screenshot-card img {
                width: 100%;
                height: 150px;
                object-fit: cover;
            }
            .screenshot-card .caption {
                padding: 10px;
                background: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Accessibility Testing Dashboard</h1>
                <p>Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </header>
            
            <div class="summary">
                <div class="summary-card" style="background-color: #e3f2fd;">
                    <h3>Total Pages Tested</h3>
                    <div class="summary-value">""" + str(len(report_files)) + """</div>
                </div>
                <div class="summary-card" style="background-color: #e8f5e9;">
                    <h3>WCAG Rules Tested</h3>
                    <div class="summary-value">""" + str(len(rule_reports)) + """</div>
                </div>
                <div class="summary-card" style="background-color: #fff3e0;">
                    <h3>Screenshots</h3>
                    <div class="summary-value">""" + str(len(screenshots)) + """</div>
                </div>
            </div>
            
            <div class="card">
                <h2>Test Reports by Page</h2>
                <table>
                    <tr>
                        <th>Page</th>
                        <th>Report</th>
                    </tr>
    """
    
    # Add report links
    for report in sorted(report_files):
        filename = os.path.basename(report)
        page_name = filename.replace("accessibility_", "").replace(".html", "")
        
        # Clean up the page name
        if page_name.startswith("www."):
            page_name = page_name[4:]
        page_name = page_name.replace("_", " ")
        
        html += f"""
                    <tr>
                        <td>{page_name}</td>
                        <td><a href="{os.path.basename(report)}" target="_blank">View Report</a></td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
            
            <div class="card">
                <h2>WCAG Rule Reports</h2>
                <table>
                    <tr>
                        <th>Rule</th>
                        <th>Report</th>
                    </tr>
    """
    
    # Add rule report links
    for report in sorted(rule_reports):
        filename = os.path.basename(report)
        rule_name = filename.replace("rule_", "").replace(".html", "")
        
        # Format the rule name
        rule_name = rule_name.replace("-", " ").title()
        
        html += f"""
                    <tr>
                        <td>{rule_name}</td>
                        <td><a href="{os.path.basename(report)}" target="_blank">View Report</a></td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
            
            <div class="card">
                <h2>Screenshots</h2>
                <p>Visual evidence of testing and identified issues.</p>
                <div class="screenshot-gallery">
    """
    
    # Add screenshot gallery
    for screenshot in sorted(screenshots)[:12]:  # Limit to first 12 screenshots
        filename = os.path.basename(screenshot)
        name = filename.replace("screenshot_", "").replace(".png", "")
        
        # Clean up the name
        if name.startswith("www."):
            name = name[4:]
        name = name.replace("_", " ")
        
        # Relative path from dashboard to screenshot
        rel_path = os.path.join("screenshots", filename)
        
        html += f"""
                    <div class="screenshot-card">
                        <img src="{rel_path}" alt="{name}">
                        <div class="caption">{name}</div>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <div class="card">
                <h2>Test Summary</h2>
                <p>This accessibility testing framework automatically scans web pages for WCAG 2.0 compliance issues.</p>
                <p>Key features:</p>
                <ul>
                    <li>Automated testing for WCAG 2.0 Level A and AA compliance</li>
                    <li>Testing of both public websites and sample pages with known issues</li>
                    <li>Comprehensive reports with screenshots</li>
                    <li>Individual rule testing for specific WCAG criteria</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write dashboard to file
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Dashboard generated at {output_file}")
    return output_file