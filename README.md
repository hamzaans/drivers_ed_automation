# Driver's Ed Course Automation 🚗

Automated script to complete driver's education courses with timed page navigation. Works on **Windows**, **Mac**, and **Linux**.

## ✨ Features

- ✅ Automatic login
- ✅ Resumes where you left off
- ✅ Waits for page timers (2-8+ minutes per page)
- ✅ Automatically clicks "next page" when timer expires
- ✅ Runs indefinitely until course completion
- ✅ Comprehensive logging
- ✅ Lightweight and stable

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** installed
- **Google Chrome** browser installed
- Your driver's ed course login credentials

### Installation

#### Windows

```powershell
# Open PowerShell in the project directory
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Mac / Linux

```bash
# Open Terminal in the project directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

1. **Edit your login credentials** in `config.py`:

```python
FIRST_NAME = "YourFirstName"
LAST_NAME = "YourLastName"
BIRTH_MONTH = "Sep"  # Three-letter month
BIRTH_DAY = "8"
BIRTH_YEAR = "2009"
```

2. **(Optional)** Edit the URL if your school is different in `config.py`

### Running

#### Windows

```powershell
venv\Scripts\activate
python drivers_ed_auto.py
```

#### Mac / Linux

```bash
source venv/bin/activate
python drivers_ed_auto.py
```

**To stop:** Press `Ctrl+C` anytime

## 📖 How It Works

1. Opens Chrome and logs into your course
2. Clicks "continue with session in progress"
3. For each page:
   - Waits for the countdown timer to expire
   - Automatically clicks "next page" button
   - Moves to next page
4. Repeats until you stop it or course is complete

## 🎥 What You'll See

```
============================================================
DRIVER'S ED COURSE AUTOMATION
============================================================

✓ LOGIN SUCCESSFUL
✓ Clicked 'continue with session' button

PAGE 1
⏳ Button is DISABLED (waiting for timer)
⏱️  Timer: 01:13 time left
⏱️  Timer: 00:45 time left
⏱️  Timer: 00:01 time left
✓ Button is now CLICKABLE!
✓ Clicked 'next page' button!

PAGE 2
⏱️  Timer: 02:34 time left
...
```

## 📝 Logs

Everything is logged to:
- **Console** - real-time progress
- **`drivers_ed.log`** - permanent record

Monitor progress:

```bash
# View live logs (Mac/Linux)
tail -f drivers_ed.log

# View logs (Windows)
Get-Content drivers_ed.log -Wait -Tail 20
```

## ⚙️ Advanced Options

### Headless Mode (No Browser Window)

Edit line 422 in `drivers_ed_auto.py`:

```python
driver = setup_driver(headless=True)  # Change False to True
```

### Run in Background

**Mac/Linux:**
```bash
nohup python drivers_ed_auto.py > output.log 2>&1 &
```

**Windows:**
Use Task Scheduler or run in a separate PowerShell window

## 🛠️ Troubleshooting

### "ChromeDriver not found"

The script should auto-download ChromeDriver. If it fails:

**Mac:**
```bash
brew install --cask chromedriver
```

**Windows:**
Download from https://chromedriver.chromium.org/ and add to PATH

**Linux:**
```bash
sudo apt install chromium-chromedriver
```

### "Module not found"

Make sure virtual environment is activated:
```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### Script Stops or Crashes

Check `drivers_ed.log` for errors. Common issues:
- Chrome version mismatch with ChromeDriver (auto-fixed by webdriver-manager)
- Network connection lost
- Course website changed layout

### Button Not Clicking

The script uses exact XPaths for your course. If the website changes:
1. Right-click the element in Chrome
2. Inspect → Copy → Copy XPath
3. Update the XPath in `drivers_ed_auto.py`

## 🔒 Safety Features

- **Per-page timeout:** 15 minutes max wait (prevents infinite loops)
- **Graceful shutdown:** Press Ctrl+C anytime
- **Progress saved:** Course progress is saved by the website
- **Auto-recovery:** Handles temporary errors

## 📂 Project Structure

```
drivers_ed_automation/
├── drivers_ed_auto.py       # Main automation script
├── config.py                 # Your login credentials
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── drivers_ed.log           # Log file (created on first run)
└── venv/                    # Virtual environment (created by you)
```

## 🤝 Contributing

Found a bug or want to improve the script? Feel free to:
1. Fork the repository
2. Make your changes
3. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational purposes. Make sure using automation complies with your course's terms of service. The script simply waits for timers and clicks buttons - it doesn't skip required waiting periods.

## 📜 License

MIT License - feel free to use and modify as needed.

## 💡 Tips

- **Run overnight:** Start it before bed and let it work through pages
- **Monitor progress:** Check `drivers_ed.log` to see how many pages completed
- **Multiple sessions:** You can stop and restart anytime - it continues where you left off
- **Keep Chrome updated:** Auto-update is handled by webdriver-manager

## 🆘 Support

If you encounter issues:

1. Check `drivers_ed.log` for error messages
2. Make sure Chrome and Python are up to date
3. Verify your credentials in `config.py`
4. Try running with browser visible (not headless) to see what's happening

---

**Happy driving! 🚗💨**
