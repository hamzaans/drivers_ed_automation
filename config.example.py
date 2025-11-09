"""
Configuration file for Driver's Ed Automation

INSTRUCTIONS:
1. Copy this file and rename it to: config.py
2. Edit config.py with your actual login credentials
3. Do NOT commit config.py to GitHub (it's in .gitignore)
"""

# Your Login Credentials - EDIT THESE!
FIRST_NAME = "YourFirstName"
LAST_NAME = "YourLastName"
BIRTH_MONTH = "Jan"  # Three-letter month abbreviation (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
BIRTH_DAY = "1"
BIRTH_YEAR = "2000"

# Course URL (change if your school uses a different URL)
URL = "https://www.va-drivercourses.com/clickIn.php?school=272"

# Browser Settings
HEADLESS = False  # Set to True to hide browser window
CHECK_INTERVAL = 2.0  # How often to check button status (seconds)
MAX_WAIT_PER_PAGE = 900  # Maximum wait time per page (seconds) - 15 minutes

