# This file is for the main accessibility scanner
# It uses axe-selenium-python to run accessibility checks

import os
import time
import uuid

from axe_selenium_python import Axe


class AccessibilityScanner:
    def __init__(self, driver):
        """
        Initialize the accessibility scanner

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.axe = Axe(self.driver)

    def inject_axe(self):
        """
        Inject the axe-core javascript into the page
        """
        # Need to inject axe-core js before we can use it
        self.axe.inject()
        print("Axe-core successfully injected")

    def _screenshot_violations(self, results):
        """
        Screenshot every violation node right after the scan returns, before
        any later page interaction (highlighting, navigation) changes what's
        on screen. Screenshots are saved under
        reports/screenshots/{run_id}/{rule_id}_{node_index}.png and the path
        is attached to that node's dict so downstream code (dashboard,
        ticket creation) can reference it - node_index only means something
        per node, so the path lives on the node, not the violation as a whole.
        """
        if not results or not results.get('violations'):
            return results

        run_id = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        screenshot_dir = os.path.join('reports', 'screenshots', run_id)
        os.makedirs(screenshot_dir, exist_ok=True)

        for violation in results['violations']:
            rule_id = violation.get('id', 'unknown')
            for node_index, node in enumerate(violation.get('nodes', [])):
                path = os.path.join(screenshot_dir, f"{rule_id}_{node_index}.png")
                try:
                    self.driver.save_screenshot(path)
                    node['screenshot_path'] = path
                except Exception as e:
                    print(f"Error saving violation screenshot: {e}")

        return results

    def run_full_scan(self):
        """
        Run a full accessibility scan with default options

        Returns:
            Dictionary with accessibility results
        """
        # Make sure axe is injected
        try:
            # Run the accessibility scan
            results = self.axe.run()
            return self._screenshot_violations(results)
        except Exception as e:
            print(f"Error running accessibility scan: {e}")
            return None
    
    def run_custom_scan(self, context=None, options=None):
        """
        Run a custom accessibility scan with specified options
        
        Args:
            context: CSS selector to limit scan scope
            options: Dictionary of axe options
        
        Returns:
            Dictionary with accessibility results
        """
        # Set default values
        if context is None:
            # Use the document body instead of 'document'
            context = "body"
        
        if options is None:
            options = {
                'runOnly': {
                    'type': 'tag',
                    'values': ['wcag2a', 'wcag2aa']
                }
            }
        
        # Run the accessibility scan with custom options
        try:
            results = self.axe.run(context=context, options=options)
            return self._screenshot_violations(results)
        except Exception as e:
            print(f"Error running custom accessibility scan: {e}")
            return None
    
    def get_violations(self, results):
        """
        Extract violations from results
        
        Args:
            results: Results from axe scan
        
        Returns:
            List of violations
        """
        if not results:
            return []
        
        return results.get('violations', [])
    
    def get_violation_count(self, results):
        """
        Count violations from results
        
        Args:
            results: Results from axe scan
        
        Returns:
            Count of violations
        """
        violations = self.get_violations(results)
        return len(violations)
    
    def print_violation_summary(self, results):
        """
        Print a summary of violations
        
        Args:
            results: Results from axe scan
        """
        violations = self.get_violations(results)
        
        if not violations:
            print("No accessibility violations found!")
            return
        
        print(f"Found {len(violations)} accessibility violations:")
        
        # Print summary of each violation
        for i, violation in enumerate(violations, 1):
            print(f"{i}. {violation.get('id', 'Unknown')}: {violation.get('help', 'No description')}")
            print(f"   Impact: {violation.get('impact', 'unknown')}")
            print(f"   Nodes affected: {len(violation.get('nodes', []))}")
            print("")