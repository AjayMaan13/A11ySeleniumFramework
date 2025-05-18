# Utility functions for report generation and screenshots

import os
import time
from datetime import datetime
from selenium import webdriver


def take_screenshot(driver, element=None, filename=None):
    """
    Take a screenshot of the page or a specific element
    
    Args:
        driver: WebDriver instance
        element: WebElement to screenshot (optional)
        filename: Name for the screenshot file (optional)
    
    Returns:
        Path to the screenshot file
    """
    # Create screenshots directory if it doesn't exist
    if not os.path.exists('reports/screenshots'):
        os.makedirs('reports/screenshots')
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"screenshot_{timestamp}.png"
    
    # Make sure filename has .png extension
    if not filename.endswith('.png'):
        filename += '.png'
    
    # Full path to save screenshot
    filepath = os.path.join('reports/screenshots', filename)
    
    try:
        if element:
            # Screenshot specific element
            element.screenshot(filepath)
        else:
            # Screenshot entire page
            driver.save_screenshot(filepath)
        
        print(f"Screenshot saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None


def highlight_element(driver, element, color="red", border=2):
    """
    Highlight an element on the page for better visibility in reports
    
    Args:
        driver: WebDriver instance
        element: WebElement to highlight
        color: Border color
        border: Border width
    """
    # Save original style
    original_style = element.get_attribute("style")
    
    # Apply highlight style
    highlight_style = f"border: {border}px solid {color};"
    driver.execute_script(
        "arguments[0].setAttribute('style', arguments[1] + arguments[2]);",
        element, original_style, highlight_style
    )
    
    # Keep highlight for a moment so it's visible in screenshots
    time.sleep(0.3)
    
    # Return to original style if needed
    # Uncomment this if you want to remove the highlight after taking screenshots
    # driver.execute_script(
    #     "arguments[0].setAttribute('style', arguments[1]);",
    #     element, original_style
    # )


def format_violation_for_report(violation):
    """
    Format a violation for display in the HTML report
    
    Args:
        violation: Violation dictionary from axe scan
    
    Returns:
        HTML string with formatted violation
    """
    # Extract useful info from violation
    violation_id = violation.get('id', 'Unknown')
    description = violation.get('help', 'No description')
    impact = violation.get('impact', 'unknown')
    help_url = violation.get('helpUrl', '#')
    nodes = violation.get('nodes', [])
    node_count = len(nodes)
    
    # Start building HTML
    html = f"""
    <div class="violation">
        <h3>{violation_id} - {impact.upper()} impact</h3>
        <p>{description}</p>
        <p><a href="{help_url}" target="_blank">More info</a></p>
        <p>Elements affected: {node_count}</p>
    """
    
    # Add node details if available
    if nodes:
        html += "<ul>"
        for node in nodes[:3]:  # Limit to first 3 for brevity
            html += f"<li>{node.get('html', 'No HTML')}</li>"
        
        if node_count > 3:
            html += f"<li>... and {node_count - 3} more elements</li>"
        
        html += "</ul>"
    
    html += "</div>"
    return html


def generate_simple_report(results, output_file="reports/accessibility_report.html"):
    """
    Generate a simple HTML report from accessibility results
    
    Args:
        results: Results from axe scan
        output_file: Path to save the HTML report
    
    Returns:
        Path to the generated report
    """
    if not results:
        print("No results to generate report from")
        return None
    
    # Extract violations
    violations = results.get('violations', [])
    passed = results.get('passes', [])
    
    # Create report directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Start building HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Accessibility Test Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .summary { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }
            .violation { background-color: #fff0f0; padding: 10px; margin: 10px 0; border-left: 4px solid #ff0000; }
            .pass { background-color: #f0fff0; padding: 5px; margin: 5px 0; border-left: 4px solid #00ff00; }
        </style>
    </head>
    <body>
        <h1>Accessibility Test Report</h1>
        <div class="summary">
            <h2>Summary</h2>
            <p>Test URL: """ + results.get('url', 'Unknown') + """</p>
            <p>Test run: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            <p>Violations: """ + str(len(violations)) + """</p>
            <p>Passed tests: """ + str(len(passed)) + """</p>
        </div>
    """
    
    if violations:
        html += """
        <h2>Violations</h2>
        """
        for violation in violations:
            html += format_violation_for_report(violation)
    else:
        html += """
        <h2>No violations found!</h2>
        """
    
    # Add a few passed tests for context
    if passed:
        html += """
        <h2>Passed tests (sample)</h2>
        """
        for test in passed[:5]:  # Just show first 5 passed tests
            html += f"""
            <div class="pass">
                <h3>{test.get('id', 'Unknown')}</h3>
                <p>{test.get('help', 'No description')}</p>
            </div>
            """
    
    # Close HTML
    html += """
    </body>
    </html>
    """
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Report generated at {output_file}")
    return output_file