# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
cd /home/hamzaans/drivers_ed_automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Test with Local HTML File

Test the navigator with the included test page to make sure everything works:

```bash
python page_navigator.py "file:///$(pwd)/test_page.html" --selector "button#nextBtn" --selector-type ID
```

You should see:
- Browser opens and loads the test page
- Page scrolls to bottom automatically
- Timer counts down (10-20 seconds)
- Button gets clicked automatically when timer expires
- Process repeats for next page

Press `Ctrl+C` to stop after testing a few pages.

## Step 3: Find Your Website's Next Button Selector

1. Open your target website in Chrome
2. Right-click the "Next" button → "Inspect"
3. In DevTools, right-click the highlighted element → Copy → Copy selector

Example: `#next-button` or `button.continue-btn`

## Step 4: Run on Your Website

Replace the URL and selector with your values:

```bash
python page_navigator.py "https://your-website.com/course/page1" --selector "YOUR_SELECTOR_HERE"
```

### Common Selector Examples:

```bash
# If button has id="nextButton"
python page_navigator.py "https://example.com" --selector "nextButton" --selector-type ID

# If button has class="next-btn"
python page_navigator.py "https://example.com" --selector "button.next-btn"

# If you need XPath
python page_navigator.py "https://example.com" --selector "//button[text()='Next']" --selector-type XPATH
```

## Step 5: Run in Background (Optional)

For long-running sessions:

```bash
# Run in headless mode in background
nohup python page_navigator.py "https://example.com" --selector "button.next" --headless > output.log 2>&1 &

# Check it's running
tail -f navigation.log

# Stop it later
pkill -f page_navigator.py
```

## Troubleshooting

### "ChromeDriver not found"
```bash
pip install webdriver-manager
# Or download ChromeDriver: https://chromedriver.chromium.org/
```

### "Button not becoming clickable"
- Double-check your selector in browser DevTools
- Try XPath instead: `--selector-type XPATH`
- Increase check interval: `--check-interval 5.0`

### "Too many consecutive failures"
- The program detected the button isn't clickable after max wait time
- Check if your selector is correct
- Verify the button actually becomes enabled on the website

## Next Steps

- See `README.md` for complete documentation
- Check `example_usage.sh` for more examples
- Monitor `navigation.log` for detailed logs

## Quick Reference

```bash
# Minimal command
python page_navigator.py URL --selector SELECTOR

# With all common options
python page_navigator.py URL \
  --selector SELECTOR \
  --selector-type CSS \
  --headless \
  --check-interval 2.0 \
  --max-wait 3600
```

That's it! You're ready to automate your page navigation. 🚀

