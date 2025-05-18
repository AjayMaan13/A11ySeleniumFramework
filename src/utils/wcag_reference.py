# Common accessibility terms and WCAG guidelines

WCAG_GLOSSARY = {
    # Core principles
    "POUR": "The four principles of accessibility: Perceivable, Operable, Understandable, Robust",
    "Perceivable": "Information and user interface components must be presentable to users in ways they can perceive",
    "Operable": "User interface components and navigation must be operable",
    "Understandable": "Information and the operation of user interface must be understandable",
    "Robust": "Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies",
    
    # Common terms
    "a11y": "Accessibility (11 letters between 'a' and 'y')",
    "assistive technology": "Software or hardware that helps users with disabilities interact with digital content",
    "screen reader": "Software that reads digital content aloud for blind or visually impaired users",
    "alt text": "Text alternative for images, used by screen readers and when images don't load",
    "ARIA": "Accessible Rich Internet Applications - a set of attributes to enhance accessibility",
    "color contrast": "The difference in brightness and color between foreground and background elements",
    
    # Common WCAG guidelines
    "1.1.1": "Non-text Content: All non-text content has a text alternative (Level A)",
    "1.3.1": "Info and Relationships: Information, structure, and relationships can be programmatically determined (Level A)",
    "1.4.3": "Contrast: Text has a contrast ratio of at least 4.5:1 (Level AA)",
    "2.1.1": "Keyboard: All functionality is available from a keyboard (Level A)",
    "2.4.1": "Bypass Blocks: Provide way to bypass blocks of content that are repeated (Level A)",
    "2.4.3": "Focus Order: Components receive focus in a meaningful order (Level A)",
    "2.4.4": "Link Purpose: The purpose of each link can be determined from the link text (Level A)",
    "3.1.1": "Language of Page: The default human language can be programmatically determined (Level A)",
    "3.2.1": "On Focus: When a component receives focus, it does not initiate a change of context (Level A)",
    "3.3.2": "Labels or Instructions: Labels or instructions are provided for user input (Level A)",
    "4.1.1": "Parsing: Content is well-formed and contains no markup errors (Level A)",
    "4.1.2": "Name, Role, Value: For all user interface components, the name, role, and value can be programmatically determined (Level A)",
    
    # Compliance levels
    "Level A": "Minimum level of conformance",
    "Level AA": "Mid-range level of conformance, addressing the major barriers",
    "Level AAA": "Highest level of conformance",
    
    # Common axe-core rules
    "image-alt": "Images must have alternate text",
    "color-contrast": "Elements must have sufficient color contrast",
    "keyboard": "Elements must be accessible by keyboard",
    "label": "Form elements must have labels",
    "heading-order": "Headings must be in ascending order",
    "link-name": "Links must have discernible text",
    "aria-roles": "ARIA roles must be valid",
    "region": "All page content should be contained by landmarks",
    
    # Assistive technologies
    "NVDA": "NonVisual Desktop Access - free screen reader for Windows",
    "JAWS": "Job Access With Speech - commercial screen reader for Windows",
    "VoiceOver": "Built-in screen reader for Apple devices",
    "TalkBack": "Built-in screen reader for Android devices",
}

# Function to get explanation of a WCAG term
def get_wcag_explanation(term):
    """
    Get explanation for a WCAG term or guideline
    
    Args:
        term: WCAG term or guideline number
    
    Returns:
        Explanation string or None if not found
    """
    return WCAG_GLOSSARY.get(term)

# Function to get all terms matching a category
def get_terms_by_category(category_prefix):
    """
    Get all terms that start with a specific prefix
    
    Args:
        category_prefix: Prefix to match (e.g., "1." for all guidelines in section 1)
    
    Returns:
        Dictionary of matching terms and explanations
    """
    return {k: v for k, v in WCAG_GLOSSARY.items() if k.startswith(category_prefix)}

# Function to get all WCAG guidelines
def get_all_wcag_guidelines():
    """
    Get all WCAG guidelines in the glossary
    
    Returns:
        Dictionary of WCAG guidelines and explanations
    """
    return {k: v for k, v in WCAG_GLOSSARY.items() if k[0].isdigit() and "." in k}