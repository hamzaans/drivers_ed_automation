#!/usr/bin/env python3
"""
Test script: Google search with infinite pagination
Searches Google, scrolls to bottom, clicks next page, repeats forever
Press Ctrl+C to stop
"""

import logging
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def smooth_scroll_to_bottom(driver, pause_time=0.5):
    """Scroll smoothly to the bottom of the page."""
    logger.info("Scrolling to bottom...")
    
    # Get total height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Scroll in increments
    current_position = 0
    scroll_increment = 500
    
    while current_position < last_height:
        current_position += scroll_increment
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.1)
    
    # Final scroll to absolute bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)
    logger.info("✓ Scrolled to bottom")


def main():
    # Search term
    SEARCH_TERM = "web automation selenium python"
    
    logger.info("=" * 60)
    logger.info("Google Search Infinite Pagination Test")
    logger.info("=" * 60)
    logger.info(f"Search term: {SEARCH_TERM}")
    logger.info("Press Ctrl+C to stop\n")
    
    # Setup Chrome
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment to run headless
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    page_count = 0
    
    try:
        # Start browser
        logger.info("Starting Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        
        # Go to Google
        logger.info("Navigating to Google...")
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Handle cookie consent if it appears
        try:
            # Try to find and click "Accept all" or "I agree" button
            accept_buttons = [
                "//button[contains(., 'Accept all')]",
                "//button[contains(., 'I agree')]",
                "//button[@id='L2AGLb']",  # Common Google consent button
            ]
            for xpath in accept_buttons:
                try:
                    button = driver.find_element(By.XPATH, xpath)
                    button.click()
                    logger.info("✓ Accepted cookies")
                    time.sleep(1)
                    break
                except:
                    pass
        except:
            pass
        
        # Find search box and enter search term
        logger.info(f"Searching for: '{SEARCH_TERM}'")
        try:
            # Try different search box selectors
            search_box = None
            selectors = [
                (By.NAME, "q"),
                (By.CSS_SELECTOR, "input[name='q']"),
                (By.CSS_SELECTOR, "textarea[name='q']"),
            ]
            
            for selector_type, selector in selectors:
                try:
                    search_box = driver.find_element(selector_type, selector)
                    break
                except:
                    continue
            
            if search_box:
                search_box.clear()
                search_box.send_keys(SEARCH_TERM)
                search_box.send_keys(Keys.RETURN)
                logger.info("✓ Search submitted")
                time.sleep(3)  # Wait for results to load
            else:
                logger.error("Could not find search box")
                return
                
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return
        
        # Main loop - infinite pagination
        while True:
            page_count += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"PAGE {page_count}")
            logger.info(f"{'='*60}")
            
            # Show current URL
            logger.info(f"URL: {driver.current_url}")
            
            # Scroll to bottom
            smooth_scroll_to_bottom(driver)
            
            # Wait a bit to view the page
            logger.info("Waiting 3 seconds before clicking next...")
            time.sleep(3)
            
            # Find and click the "Next" button
            logger.info("Looking for 'Next' button...")
            next_button = None
            
            # Try multiple selectors for the next button
            next_selectors = [
                (By.ID, "pnnext"),  # Standard Google next button ID
                (By.CSS_SELECTOR, "a#pnnext"),
                (By.XPATH, "//a[@id='pnnext']"),
                (By.XPATH, "//a[contains(@aria-label, 'Next')]"),
                (By.XPATH, "//span[text()='Next']/parent::a"),
            ]
            
            for selector_type, selector in next_selectors:
                try:
                    next_button = driver.find_element(selector_type, selector)
                    if next_button.is_displayed():
                        break
                except:
                    continue
            
            if next_button:
                try:
                    # Scroll button into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(0.5)
                    
                    # Click the button
                    next_button.click()
                    logger.info("✓ Clicked 'Next' button")
                    
                    # Wait for new page to load
                    time.sleep(3)
                    
                except Exception as e:
                    logger.error(f"Failed to click next button: {e}")
                    
                    # Try JavaScript click as fallback
                    try:
                        logger.info("Trying JavaScript click...")
                        driver.execute_script("arguments[0].click();", next_button)
                        logger.info("✓ JavaScript click successful")
                        time.sleep(3)
                    except Exception as e2:
                        logger.error(f"JavaScript click also failed: {e2}")
                        logger.warning("Could not proceed to next page. Stopping.")
                        break
            else:
                logger.warning("⚠ No 'Next' button found - might be on last page or selector changed")
                logger.info("Waiting 5 seconds and will try again...")
                time.sleep(5)
                # Don't break, just try again in case it loads
            
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Keyboard interrupt received (Ctrl+C)")
        logger.info(f"Total pages visited: {page_count}")
        
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}", exc_info=True)
        
    finally:
        if driver:
            logger.info("\nClosing browser...")
            try:
                driver.quit()
                logger.info("✓ Browser closed")
            except:
                pass
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Session Summary:")
        logger.info(f"  - Pages visited: {page_count}")
        logger.info(f"  - Search term: '{SEARCH_TERM}'")
        logger.info(f"{'='*60}")


if __name__ == '__main__':
    main()

