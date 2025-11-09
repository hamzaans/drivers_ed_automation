# Driver's Ed Course Automation - Quick Guide

## 🎯 What This Does

This script automatically completes your driver's ed course by:
1. ✅ Logging in with your credentials
2. ✅ Clicking "continue with session in progress"
3. ✅ Scrolling to the bottom of each page
4. ✅ Waiting for the timer to expire (2 mins, 8 mins, whatever)
5. ✅ Clicking "next page" when the button becomes active
6. ✅ Repeating until you stop it with Ctrl+C

## 🚀 How to Run

```bash
cd /home/hamzaans/drivers_ed_automation
source venv/bin/activate
python drivers_ed_auto.py
```

**To stop:** Press `Ctrl+C` anytime

## 📊 What You'll See

```
============================================================
DRIVER'S ED COURSE AUTOMATION
============================================================
Press Ctrl+C to stop anytime

============================================================
LOGGING IN
============================================================
Opening https://www.va-drivercourses.com/clickIn.php?school=272
✓ Clicked 'Log In' button
✓ Entered first name: Ismail
✓ Entered last name: Ansari
✓ Selected month: Sep
✓ Selected day: 8
✓ Selected year: 2009
✓ Clicked Login submit button
✓ LOGIN SUCCESSFUL

============================================================
LOOKING FOR 'CONTINUE WITH SESSION' BUTTON
============================================================
✓ Scrolled to bottom
✓ Clicked 'continue with session' button

============================================================
STARTING PAGE NAVIGATION
============================================================

============================================================
PAGE 1
============================================================
URL: https://...
✓ Scrolled to bottom

============================================================
WAITING FOR TIMER TO EXPIRE
============================================================
⏱️  Timer: 01:13 time left
⏱️  Timer: 01:09 time left
⏱️  Timer: 00:58 time left
...
⏱️  Timer: 00:01 time left
✓ Timer expired after 73.2 seconds!
Clicking 'next page' button...
✓ Clicked 'next page' button!
✓ Completed page 1

============================================================
PAGE 2
============================================================
...
```

## ⚙️ Configuration

Your login info is in the script (lines 22-27):

```python
FIRST_NAME = "Ismail"
LAST_NAME = "Ansari"
BIRTH_MONTH = "Sep"
BIRTH_DAY = "8"
BIRTH_YEAR = "2009"
```

## 🎨 Run Without Browser Window (Headless)

Edit line 190 in `drivers_ed_auto.py`:

```python
driver = setup_driver(headless=True)  # Change False to True
```

Or leave it as `False` to watch it work!

## 📝 Logs

Everything is logged to:
- Console (what you see)
- `drivers_ed.log` file (permanent record)

## 🛑 Stopping

Press `Ctrl+C` anytime to stop. It will:
- Show you how many pages were completed
- Close the browser cleanly
- Save your progress

## ⚠️ Important Notes

1. **Don't close the browser manually** - let the script do it when you press Ctrl+C
2. **The script waits indefinitely** for each timer - no matter how long it takes
3. **Maximum 15 minutes per page** - safety timeout in case something breaks
4. **Your progress is saved** by the website, so you can stop and restart anytime

## 💡 Tips

- Run it in the evening and let it work overnight
- You can minimize the browser window
- Check `drivers_ed.log` to see progress history
- The script will keep going until all pages are done or you stop it

## 🎉 That's It!

Just run the command and let it do its thing. Press Ctrl+C when you're done!

```bash
python drivers_ed_auto.py
```

