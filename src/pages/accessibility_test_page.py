# Custom page object for testing demo pages
# This extends the BasePage class with specific methods for accessibility testing

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.pages.base_page import BasePage


class AccessibilityTestPage(BasePage):
    """
    Page object for accessibility testing with additional methods
    specifically for testing WCAG compliance
    """
    
    def __init__(self, driver):
        """Initialize the page object"""
        super().__init__(driver)
        
        # Common locators for accessibility testing
        self.locators = {
            "images": (By.TAG_NAME, "img"),
            "links": (By.TAG_NAME, "a"),
            "buttons": (By.TAG_NAME, "button"),
            "form_fields": (By.CSS_SELECTOR, "input, select, textarea"),
            "headings": (By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6"),
            "tables": (By.TAG_NAME, "table"),
        }
    
    def test_keyboard_navigation(self):
        """
        Test keyboard navigation (WCAG 2.1.1)
        
        Returns:
            Dictionary with results
        """
        results = {
            "can_tab_through": False,
            "focusable_elements": 0,
            "tab_trap": False,
            "errors": []
        }
        
        try:
            # Send body element a tab key to start
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
            
            # Count how many elements we can tab through
            focusable_elements = 0
            max_elements = 50  # Safety limit
            
            # Keep track of elements we've seen to detect loops
            seen_elements = set()
            current_element = None
            
            # Tab through elements
            for i in range(max_elements):
                # Get the currently focused element
                current_element = self.driver.switch_to.active_element
                
                # If we've seen this element before, we might be in a tab trap
                element_id = current_element.id
                if element_id in seen_elements:
                    results["tab_trap"] = True
                    results["errors"].append(f"Tab trap detected after {i} tabs")
                    break
                
                seen_elements.add(element_id)
                focusable_elements += 1
                
                # Send tab key
                current_element.send_keys(Keys.TAB)
            
            results["focusable_elements"] = focusable_elements
            results["can_tab_through"] = focusable_elements > 0
            
        except Exception as e:
            results["errors"].append(f"Error during keyboard navigation test: {str(e)}")
        
        return results
    
    def check_image_alt_text(self):
        """
        Check for images without alt text (WCAG 1.1.1)
        
        Returns:
            Dictionary with results
        """
        results = {
            "total_images": 0,
            "missing_alt": 0,
            "empty_alt": 0,
            "images_with_valid_alt": 0,
            "problem_images": []
        }
        
        try:
            # Find all images
            images = self.find_elements(*self.locators["images"])
            results["total_images"] = len(images)
            
            # Check each image
            for img in images:
                # Check if alt attribute exists
                if not img.get_attribute("alt"):
                    if img.get_attribute("alt") == "":
                        # Empty alt is ok for decorative images, but we'll count them
                        results["empty_alt"] += 1
                    else:
                        # Missing alt attribute
                        results["missing_alt"] += 1
                        results["problem_images"].append({
                            "element": img,
                            "issue": "Missing alt attribute",
                            "html": img.get_attribute("outerHTML")
                        })
                else:
                    # Has alt text, check if it's just "image" or similar
                    alt_text = img.get_attribute("alt").lower()
                    if alt_text in ["image", "photo", "picture", "img"]:
                        results["missing_alt"] += 1
                        results["problem_images"].append({
                            "element": img,
                            "issue": f"Generic alt text: {alt_text}",
                            "html": img.get_attribute("outerHTML")
                        })
                    else:
                        results["images_with_valid_alt"] += 1
        
        except Exception as e:
            results["error"] = f"Error checking alt text: {str(e)}"
        
        return results
    
    def check_form_labels(self):
        """
        Check for form controls without labels (WCAG 3.3.2)
        
        Returns:
            Dictionary with results
        """
        results = {
            "total_form_fields": 0,
            "fields_without_labels": 0,
            "fields_with_labels": 0,
            "problem_fields": []
        }
        
        try:
            # Find all form fields
            form_fields = self.find_elements(*self.locators["form_fields"])
            results["total_form_fields"] = len(form_fields)
            
            # Check each field
            for field in form_fields:
                field_id = field.get_attribute("id")
                
                if not field_id:
                    # If no ID, can't have a proper label
                    results["fields_without_labels"] += 1
                    results["problem_fields"].append({
                        "element": field,
                        "issue": "No ID attribute for label association",
                        "html": field.get_attribute("outerHTML")
                    })
                    continue
                
                # Check if there's a label with for=id
                label_selector = f"label[for='{field_id}']"
                labels = self.driver.find_elements(By.CSS_SELECTOR, label_selector)
                
                if not labels:
                    # No label found
                    results["fields_without_labels"] += 1
                    results["problem_fields"].append({
                        "element": field,
                        "issue": f"No label found for field with ID '{field_id}'",
                        "html": field.get_attribute("outerHTML")
                    })
                else:
                    results["fields_with_labels"] += 1
        
        except Exception as e:
            results["error"] = f"Error checking form labels: {str(e)}"
        
        return results
    
    def check_heading_structure(self):
        """
        Check for proper heading structure (WCAG 1.3.1)
        
        Returns:
            Dictionary with results
        """
        results = {
            "total_headings": 0,
            "heading_levels_used": [],
            "has_h1": False,
            "proper_sequence": True,
            "issues": []
        }
        
        try:
            # Find all headings
            headings = self.find_elements(*self.locators["headings"])
            results["total_headings"] = len(headings)
            
            # Track heading levels in order
            heading_sequence = []
            
            # Check each heading
            for heading in headings:
                tag_name = heading.tag_name.lower()
                level = int(tag_name[1])
                
                heading_sequence.append(level)
                
                # Track which levels are used
                if level not in results["heading_levels_used"]:
                    results["heading_levels_used"].append(level)
            
            # Sort heading levels
            results["heading_levels_used"].sort()
            
            # Check if has h1
            results["has_h1"] = 1 in results["heading_levels_used"]
            
            # Check sequence
            prev_level = 0
            for i, level in enumerate(heading_sequence):
                if i == 0 and level != 1:
                    results["proper_sequence"] = False
                    results["issues"].append(f"First heading is not h1, found h{level}")
                
                if level > prev_level + 1 and prev_level > 0:
                    results["proper_sequence"] = False
                    results["issues"].append(f"Heading level jumped from h{prev_level} to h{level}")
                
                prev_level = level
        
        except Exception as e:
            results["error"] = f"Error checking heading structure: {str(e)}"
        
        return results
    
    def run_manual_accessibility_checks(self):
        """
        Run manual accessibility checks in addition to axe-core
        
        Returns:
            Dictionary with all manual test results
        """
        results = {
            "keyboard_navigation": self.test_keyboard_navigation(),
            "image_alt_text": self.check_image_alt_text(),
            "form_labels": self.check_form_labels(),
            "heading_structure": self.check_heading_structure()
        }
        
        return results