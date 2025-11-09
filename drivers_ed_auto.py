#!/usr/bin/env python3
"""
Automated Driver's Ed Course Navigator
Handles login, timer waits, and automatic page progression
"""

import logging
import time
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    StaleElementReferenceException
)

# Import configuration
try:
    from config import (
        URL, FIRST_NAME, LAST_NAME, BIRTH_MONTH, BIRTH_DAY, BIRTH_YEAR,
        HEADLESS, CHECK_INTERVAL, MAX_WAIT_PER_PAGE
    )
except ImportError:
    print("ERROR: config.py not found!")
    print("Please create config.py with your login credentials.")
    print("See README.md for instructions.")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drivers_ed.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def setup_driver():
    """Initialize Chrome WebDriver"""
    chrome_options = Options()
    
    if HEADLESS:
        chrome_options.add_argument('--headless')
        logger.info("Running in headless mode")
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    return driver


def smooth_scroll_to_bottom(driver, pause_time=0.5):
    """Scroll smoothly to bottom of page"""
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        scroll_increment = 500
        
        while current_position < last_height:
            current_position += scroll_increment
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(0.1)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        logger.info("✓ Scrolled to bottom")
    except Exception as e:
        logger.warning(f"Scroll error: {e}")


def login(driver):
    """Handle login process"""
    logger.info("=" * 60)
    logger.info("LOGGING IN")
    logger.info("=" * 60)
    
    try:
        # Navigate to site
        logger.info(f"Opening {URL}")
        driver.get(URL)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "button"))
        )
        
        # Click "Log In" button
        logger.info("Looking for 'Log In' button...")
        login_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Log In')] | //a[contains(text(), 'Log In')]")
        
        if not login_buttons:
            logger.info("Trying alternate login button selector...")
            login_buttons = driver.find_elements(By.CSS_SELECTOR, "button, a")
            for btn in login_buttons:
                if "log in" in btn.text.lower():
                    login_buttons = [btn]
                    break
        
        if login_buttons:
            login_buttons[0].click()
            logger.info("✓ Clicked 'Log In' button")
            
            # Wait for login form to appear
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
        else:
            logger.info("Login button not found, checking if login form is already visible...")
        
        # Fill in first name
        logger.info("Filling in First Name...")
        first_name_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text'] | //input[contains(@placeholder, 'First')] | //input[@name='firstName'] | //input[@id='firstName']"))
        )
        first_name_field.clear()
        first_name_field.send_keys(FIRST_NAME)
        logger.info(f"✓ Entered first name: {FIRST_NAME}")
        
        # Fill in last name
        logger.info("Filling in Last Name...")
        last_name_fields = driver.find_elements(By.XPATH, "//input[@type='text']")
        if len(last_name_fields) >= 2:
            last_name_field = last_name_fields[1]
        else:
            last_name_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Last')] | //input[@name='lastName'] | //input[@id='lastName']")
        last_name_field.clear()
        last_name_field.send_keys(LAST_NAME)
        logger.info(f"✓ Entered last name: {LAST_NAME}")
        
        # Select birthday - Month
        logger.info("Selecting birth month...")
        month_selects = driver.find_elements(By.TAG_NAME, "select")
        if len(month_selects) >= 1:
            month_select = Select(month_selects[0])
            month_select.select_by_visible_text(BIRTH_MONTH)
            logger.info(f"✓ Selected month: {BIRTH_MONTH}")
        
        # Select birthday - Day
        if len(month_selects) >= 2:
            day_select = Select(month_selects[1])
            day_select.select_by_visible_text(BIRTH_DAY)
            logger.info(f"✓ Selected day: {BIRTH_DAY}")
        
        # Select birthday - Year
        if len(month_selects) >= 3:
            year_select = Select(month_selects[2])
            year_select.select_by_visible_text(BIRTH_YEAR)
            logger.info(f"✓ Selected year: {BIRTH_YEAR}")
        
        # Click Login button in the modal
        logger.info("Clicking Login button...")
        login_submit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Login')] | //button[@type='submit']")
        if login_submit_buttons:
            login_submit_buttons[-1].click()  # Use last one (in the modal)
            logger.info("✓ Clicked Login submit button")
            
            # Wait for navigation (check URL change or new page element)
            time.sleep(2)
        else:
            logger.error("Could not find login submit button")
            return False
        
        logger.info("✓ LOGIN SUCCESSFUL")
        return True
        
    except Exception as e:
        logger.error(f"Login failed: {e}", exc_info=True)
        return False


def click_continue_session(driver):
    """Click 'continue with session in progress' button"""
    logger.info("\n" + "=" * 60)
    logger.info("LOOKING FOR 'CONTINUE WITH SESSION' BUTTON")
    logger.info("=" * 60)
    
    try:
        # Give page a moment to fully load
        time.sleep(1)
        
        # Try the EXACT XPath first
        continue_button = None
        
        try:
            logger.info("Looking for button at exact XPath...")
            continue_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[3]/form/input[2]")
            button_value = continue_button.get_attribute('value')
            logger.info(f"✓ Found button at exact location: '{button_value}'")
        except NoSuchElementException:
            logger.info("Button not found at exact XPath, trying fallback methods...")
            
            # Fallback: Find ALL clickable elements
            logger.info("Scanning page for clickable elements...")
            
            all_elements = []
            all_elements.extend(driver.find_elements(By.TAG_NAME, "button"))
            all_elements.extend(driver.find_elements(By.CSS_SELECTOR, "input[type='button']"))
            all_elements.extend(driver.find_elements(By.CSS_SELECTOR, "input[type='submit']"))
            all_elements.extend(driver.find_elements(By.TAG_NAME, "a"))
            
            logger.info(f"Found {len(all_elements)} clickable element(s) on page")
            
            # Log what each element says (first 10 only)
            for i, elem in enumerate(all_elements[:10]):
                try:
                    elem_text = elem.text.strip()
                    elem_value = elem.get_attribute('value')
                    display_text = elem_text or elem_value or "(no text)"
                    if display_text and display_text != "(no text)":
                        logger.info(f"  Element {i+1}: '{display_text}' (tag: {elem.tag_name})")
                except:
                    pass
            
            # Search through all elements
            for elem in all_elements:
                try:
                    elem_text = (elem.text or elem.get_attribute('value') or '').lower().strip()
                    if "continue" in elem_text and "session" in elem_text:
                        logger.info(f"✓ Found continue element: '{elem.text or elem.get_attribute('value')}'")
                        continue_button = elem
                        break
                except:
                    pass
        
        # Click the button if found
        if continue_button:
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
            time.sleep(0.3)
            
            # Click it
            try:
                continue_button.click()
                logger.info("✓ Clicked 'continue with session' button")
            except:
                # Try JavaScript click if normal click fails
                logger.info("Normal click failed, trying JavaScript click...")
                driver.execute_script("arguments[0].click();", continue_button)
                logger.info("✓ JavaScript click successful")
            
            # Wait for page to load
            time.sleep(2)
            logger.info(f"New URL: {driver.current_url}")
            return True
        else:
            logger.warning("❌ 'Continue with session' button not found")
            logger.info("\nCurrent URL: " + driver.current_url)
            
            # Save page source for debugging
            logger.info("Saving page source to 'debug_page.html' for inspection...")
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            
            return True  # Continue anyway in case we're already in the course
            
    except Exception as e:
        logger.error(f"Error clicking continue button: {e}", exc_info=True)
        return False


def check_timer_and_button(driver):
    """
    Check if timer is still running or if next page button is clickable
    Returns: (timer_active, button_clickable, time_remaining)
    """
    try:
        # Check the EXACT timer element
        timer_active = False
        time_remaining = "unknown"
        
        try:
            timer_elem = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/table/tbody/tr/td")
            timer_text = timer_elem.text.strip()
            
            # Check if timer contains "time left" and actual countdown
            if timer_text and ('time left' in timer_text.lower() or ':' in timer_text):
                # Make sure it's an actual countdown (has numbers and colon)
                if ':' in timer_text and len(timer_text) < 30:
                    timer_active = True
                    time_remaining = timer_text
        except NoSuchElementException:
            # Timer element doesn't exist, might mean it's expired
            pass
        except Exception as e:
            logger.debug(f"Timer check error: {e}")
        
        # Check the EXACT next page button
        button_clickable = False
        
        try:
            next_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/table[2]/tbody/tr[5]/td[2]/input")
            
            # Check if button is displayed
            if next_button.is_displayed():
                # Check if enabled (not disabled)
                disabled_attr = next_button.get_attribute('disabled')
                
                # Button is clickable if:
                # 1. No disabled attribute, OR
                # 2. Disabled attribute is not "true" or "disabled"
                if not disabled_attr or (disabled_attr != 'true' and disabled_attr != 'disabled'):
                    button_clickable = True
                    
        except NoSuchElementException:
            # Button doesn't exist on this page
            pass
        except Exception as e:
            logger.debug(f"Button check error: {e}")
        
        return timer_active, button_clickable, time_remaining
        
    except Exception as e:
        logger.debug(f"Error checking timer/button: {e}")
        return False, False, "error"


def wait_for_timer_and_click_next(driver):
    """Wait for timer to expire and click next page button"""
    logger.info("\n" + "=" * 60)
    logger.info("WAITING FOR TIMER TO EXPIRE")
    logger.info("=" * 60)
    
    check_count = 0
    start_time = time.time()
    last_time_remaining = None
    last_button_state = None
    
    while True:
        check_count += 1
        elapsed = time.time() - start_time
        
        # Check status
        timer_active, button_clickable, time_remaining = check_timer_and_button(driver)
        
        # Log if time remaining changed
        if time_remaining != last_time_remaining and time_remaining != "unknown":
            logger.info(f"⏱️  Timer: {time_remaining}")
            last_time_remaining = time_remaining
        
        # Log button state changes
        if button_clickable != last_button_state:
            if button_clickable:
                logger.info("✓ Button is now CLICKABLE!")
            else:
                logger.info("⏳ Button is DISABLED (waiting for timer)")
            last_button_state = button_clickable
        
        # If button is clickable, click it!
        if button_clickable:
            logger.info(f"✓ Timer expired after {elapsed:.1f} seconds!")
            logger.info("Clicking 'next page' button...")
            
            try:
                # Find the EXACT next page button using the provided XPath
                next_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/table[2]/tbody/tr[5]/td[2]/input")
                
                # Scroll button into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(0.3)
                
                # Try clicking
                try:
                    next_button.click()
                    logger.info("✓ Clicked 'next page' button!")
                except:
                    # Try JavaScript click if normal click fails
                    logger.info("Normal click failed, trying JavaScript click...")
                    driver.execute_script("arguments[0].click();", next_button)
                    logger.info("✓ JavaScript click successful")
                
                # Wait for next page to load
                time.sleep(2)
                return True
                    
            except NoSuchElementException:
                logger.error("Next button not found at expected location")
                return False
            except Exception as e:
                logger.error(f"Error clicking next button: {e}")
                return False
        
        # Log progress periodically
        if check_count % 15 == 0:  # Every 30 seconds (2s * 15)
            logger.info(f"Still waiting... {elapsed:.0f}s elapsed (Check #{check_count})")
        
        # Safety check - don't wait more than MAX_WAIT_PER_PAGE
        if elapsed > MAX_WAIT_PER_PAGE:
            logger.warning(f"Exceeded {MAX_WAIT_PER_PAGE/60:.0f} minute wait time on this page")
            return False
        
        # Wait before next check
        time.sleep(CHECK_INTERVAL)


def main():
    """Main execution"""
    logger.info("\n" + "=" * 60)
    logger.info("DRIVER'S ED COURSE AUTOMATION")
    logger.info("=" * 60)
    logger.info("Press Ctrl+C to stop anytime\n")
    
    driver = None
    page_count = 0
    
    try:
        # Setup browser
        driver = setup_driver()
        
        # Login
        if not login(driver):
            logger.error("Login failed, stopping.")
            return
        
        # Click continue with session
        click_continue_session(driver)
        
        # Main loop - process pages
        logger.info("\n" + "=" * 60)
        logger.info("STARTING PAGE NAVIGATION")
        logger.info("=" * 60)
        
        while True:
            page_count += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"PAGE {page_count}")
            logger.info(f"{'='*60}")
            logger.info(f"URL: {driver.current_url}")
            
            # Wait for timer and click next
            success = wait_for_timer_and_click_next(driver)
            
            if not success:
                logger.warning("Failed to proceed to next page")
                # Try to continue anyway
                time.sleep(5)
            
            logger.info(f"✓ Completed page {page_count}")
        
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Stopped by user (Ctrl+C)")
        logger.info(f"Total pages completed: {page_count}")
        
    except Exception as e:
        logger.error(f"\n❌ Error: {e}", exc_info=True)
        
    finally:
        if driver:
            logger.info("\nClosing browser...")
            try:
                driver.quit()
                logger.info("✓ Browser closed")
            except:
                pass
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Session Summary")
        logger.info(f"  Pages completed: {page_count}")
        logger.info(f"{'='*60}")


if __name__ == '__main__':
    main()

