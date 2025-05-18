# Sample HTML files with accessibility issues for testing

# Missing Alt Text HTML
MISSING_ALT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Missing Alt Text Example</title>
</head>
<body>
    <h1>Missing Alt Text Example</h1>
    <p>This page contains images with missing or inadequate alt text.</p>
    
    <!-- Image with no alt attribute -->
    <img src="https://via.placeholder.com/150" width="150" height="150">
    
    <!-- Image with empty alt attribute -->
    <img src="https://via.placeholder.com/150" alt="" width="150" height="150">
    
    <!-- Image with generic unhelpful alt attribute -->
    <img src="https://via.placeholder.com/150" alt="image" width="150" height="150">
    
    <!-- Decorative image correctly using empty alt -->
    <img src="https://via.placeholder.com/50" alt="" width="50" height="50" style="border: 1px solid #ddd;">
    
    <!-- Example of proper alt text for comparison -->
    <img src="https://via.placeholder.com/150" alt="Blue square placeholder image" width="150" height="150">
</body>
</html>
"""

# Contrast Issues HTML
CONTRAST_ISSUES_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contrast Issues Example</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        .low-contrast-1 {
            color: #aaa;
            background-color: #fff;
        }
        .low-contrast-2 {
            color: #999;
            background-color: #eee;
        }
        .low-contrast-3 {
            color: #55a;
            background-color: #338;
        }
        .good-contrast {
            color: #000;
            background-color: #fff;
        }
    </style>
</head>
<body>
    <h1>Contrast Issues Example</h1>
    <p>This page contains text with various contrast issues.</p>
    
    <div class="low-contrast-1">
        <p>This text has low contrast (light gray on white background).</p>
    </div>
    
    <div class="low-contrast-2">
        <p>This text also has low contrast (gray on light gray background).</p>
    </div>
    
    <div class="low-contrast-3">
        <p>This text has low contrast with similar hues (blue on blue).</p>
    </div>
    
    <div class="good-contrast">
        <p>This text has good contrast (black on white background).</p>
    </div>
</body>
</html>
"""

# Form Labels HTML
FORM_LABELS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Labels Example</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <h1>Form Labels Example</h1>
    <p>This page contains forms with various labeling issues.</p>
    
    <h2>Form with Missing Labels</h2>
    <form>
        <div class="form-group">
            <!-- Input without label -->
            <input type="text" placeholder="Name" name="name">
        </div>
        
        <div class="form-group">
            <!-- Input with placeholder but no label -->
            <input type="email" placeholder="Email Address" name="email">
        </div>
        
        <div class="form-group">
            <!-- Select without label -->
            <select name="country">
                <option value="">Select Country</option>
                <option value="us">United States</option>
                <option value="ca">Canada</option>
                <option value="uk">United Kingdom</option>
            </select>
        </div>
        
        <button type="submit">Submit</button>
    </form>
    
    <h2>Form with Proper Labels</h2>
    <form>
        <div class="form-group">
            <label for="name2">Name</label>
            <input id="name2" type="text" name="name">
        </div>
        
        <div class="form-group">
            <label for="email2">Email Address</label>
            <input id="email2" type="email" name="email">
        </div>
        
        <div class="form-group">
            <label for="country2">Country</label>
            <select id="country2" name="country">
                <option value="">Select Country</option>
                <option value="us">United States</option>
                <option value="ca">Canada</option>
                <option value="uk">United Kingdom</option>
            </select>
        </div>
        
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# Dictionary mapping test cases to HTML content
TEST_PAGES = {
    "missing_alt.html": MISSING_ALT_HTML,
    "contrast_issues.html": CONTRAST_ISSUES_HTML,
    "form_labels.html": FORM_LABELS_HTML
}

# Function to write the HTML files to the proper location
def create_test_pages():
    """
    Create test HTML pages in the sites directory
    
    Returns:
        List of file paths created
    """
    import os
    
    # Create the directory if it doesn't exist
    os.makedirs("tests/sites", exist_ok=True)
    
    created_files = []
    
    # Write each test page to a file
    for filename, content in TEST_PAGES.items():
        filepath = os.path.join("tests/sites", filename)
        
        with open(filepath, "w") as f:
            f.write(content)
        
        created_files.append(filepath)
        print(f"Created test page: {filepath}")
    
    return created_files