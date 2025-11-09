#!/bin/bash
# Quick activation script for the virtual environment

cd /home/hamzaans/drivers_ed_automation
source venv/bin/activate

echo "✓ Virtual environment activated!"
echo "✓ Python: $(python --version)"
echo "✓ Selenium installed and ready"
echo ""
echo "You can now run:"
echo "  python page_navigator.py --help"
echo ""
echo "To deactivate later, just type: deactivate"

