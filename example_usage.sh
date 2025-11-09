#!/bin/bash
# Example usage script for page_navigator.py

# Example 1: Basic usage with CSS selector
# python page_navigator.py "https://your-website.com/course" --selector "button#next-button"

# Example 2: Using XPath for more complex selection
# python page_navigator.py "https://your-website.com/course" \
#   --selector "//button[contains(@class, 'next') and not(@disabled)]" \
#   --selector-type XPATH

# Example 3: Running in headless mode (no browser window) with custom check interval
# python page_navigator.py "https://your-website.com/course" \
#   --selector "button.next-page" \
#   --headless \
#   --check-interval 3.0

# Example 4: Testing with local HTML file
# python page_navigator.py "file:///$(pwd)/test_page.html" \
#   --selector "button#nextBtn" \
#   --selector-type ID

# Example 5: Long-running with extended max wait time
# python page_navigator.py "https://your-website.com/course" \
#   --selector "button.continue" \
#   --max-wait 7200 \
#   --headless

echo "Please edit this file and uncomment the example you want to use."
echo "Don't forget to replace the URL and selector with your actual values!"

