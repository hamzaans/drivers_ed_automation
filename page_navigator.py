#!/usr/bin/env python3
"""
Web Page Navigator with Dynamic Timer Support

This script automates clicking through pages on a website where the "next" button
is disabled until a timer expires. It handles variable timer durations and runs
indefinitely without hard timeouts.
"""

import logging
import time
import sys
from datetime import datetime
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('navigation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PageNavigator:
    """Handles automated navigation through pages with timed next buttons."""
    
    def __init__(
        self,
        url: str,
        next_button_selector: str,
        selector_type: str = "CSS",
        headless: bool = False,
        scroll_pause: float = 0.5,
        check_interval: float = 2.0,
        max_wait_per_page: int = 3600  # 1 hour max per page
    ):
        """
        Initialize the navigator.
        
        Args:
            url: The starting URL
            next_button_selector: Selector for the next button
            selector_type: Type of selector - "CSS", "XPATH", "ID", "CLASS", etc.
            headless: Whether to run browser in headless mode
            scroll_pause: Time to pause after scrolling
            check_interval: How often to check if button is clickable (seconds)
            max_wait_per_page: Maximum time to wait on a single page (seconds)
        """
        self.url = url
        self.next_button_selector = next_button_selector
        self.selector_type = selector_type.upper()
        self.headless = headless
        self.scroll_pause = scroll_pause
        self.check_interval = check_interval
        self.max_wait_per_page = max_wait_per_page
        
        self.driver: Optional[webdriver.Chrome] = None
        self.page_count = 0
        self.total_wait_time = 0
        
    def _get_by_type(self):
        """Convert selector type string to Selenium By type."""
        selector_map = {
            "CSS": By.CSS_SELECTOR,
            "XPATH": By.XPATH,
            "ID": By.ID,
            "CLASS": By.CLASS_NAME,
            "NAME": By.NAME,
            "TAG": By.TAG_NAME,
            "LINK_TEXT": By.LINK_TEXT,
            "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
        }
        return selector_map.get(self.selector_type, By.CSS_SELECTOR)
    
    def setup_driver(self):
        """Initialize the Chrome WebDriver with appropriate options."""
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
            logger.info("Running in headless mode")
        
        # Additional options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Keep browser alive even if connection is lost temporarily
        chrome_options.add_argument('--disable-hang-monitor')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(5)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page smoothly."""
        try:
            # Get initial scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scroll down in increments for smooth scrolling
            current_position = 0
            scroll_increment = 500
            
            while current_position < last_height:
                current_position += scroll_increment
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(0.1)
            
            # Final scroll to absolute bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.scroll_pause)
            
            logger.info("Scrolled to bottom of page")
        except Exception as e:
            logger.warning(f"Error while scrolling: {e}")
    
    def is_button_clickable(self) -> bool:
        """
        Check if the next button is clickable.
        
        Returns:
            True if button is clickable, False otherwise
        """
        try:
            button = self.driver.find_element(self._get_by_type(), self.next_button_selector)
            
            # Check if element is displayed and enabled
            if not button.is_displayed() or not button.is_enabled():
                return False
            
            # Check if button has disabled attribute or class
            disabled_attr = button.get_attribute('disabled')
            if disabled_attr == 'true' or disabled_attr == 'disabled':
                return False
            
            # Check for common disabled classes
            classes = button.get_attribute('class') or ''
            if 'disabled' in classes.lower():
                return False
            
            # Check for pointer-events: none in style
            style = button.get_attribute('style') or ''
            if 'pointer-events: none' in style or 'pointer-events:none' in style:
                return False
            
            return True
            
        except (NoSuchElementException, StaleElementReferenceException) as e:
            logger.debug(f"Button not found or stale: {e}")
            return False
        except Exception as e:
            logger.warning(f"Error checking button clickability: {e}")
            return False
    
    def wait_for_button_clickable(self) -> bool:
        """
        Wait for the next button to become clickable.
        Polls continuously without hard timeout on the actual wait.
        
        Returns:
            True if button became clickable, False if max_wait_per_page exceeded
        """
        start_time = time.time()
        check_count = 0
        
        logger.info("Waiting for next button to become clickable...")
        
        while True:
            check_count += 1
            elapsed = time.time() - start_time
            
            # Check if we've exceeded max wait time for this page
            if elapsed > self.max_wait_per_page:
                logger.warning(
                    f"Max wait time ({self.max_wait_per_page}s) exceeded on page {self.page_count + 1}"
                )
                return False
            
            # Check button status
            if self.is_button_clickable():
                logger.info(
                    f"Button became clickable after {elapsed:.1f} seconds "
                    f"({check_count} checks)"
                )
                return True
            
            # Log progress periodically
            if check_count % 30 == 0:  # Every minute with 2-second intervals
                logger.info(
                    f"Still waiting... {elapsed:.0f}s elapsed "
                    f"(Check #{check_count})"
                )
            
            # Wait before next check
            time.sleep(self.check_interval)
    
    def click_next_button(self) -> bool:
        """
        Click the next button.
        
        Returns:
            True if successfully clicked, False otherwise
        """
        try:
            button = self.driver.find_element(self._get_by_type(), self.next_button_selector)
            
            # Scroll button into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.5)
            
            # Try clicking
            button.click()
            logger.info("Successfully clicked next button")
            
            # Wait a bit for page to start loading
            time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to click next button: {e}")
            
            # Try JavaScript click as fallback
            try:
                logger.info("Attempting JavaScript click...")
                button = self.driver.find_element(self._get_by_type(), self.next_button_selector)
                self.driver.execute_script("arguments[0].click();", button)
                logger.info("JavaScript click successful")
                time.sleep(1)
                return True
            except Exception as e2:
                logger.error(f"JavaScript click also failed: {e2}")
                return False
    
    def navigate_to_next_page(self) -> bool:
        """
        Complete process of navigating to the next page.
        
        Returns:
            True if successfully navigated, False otherwise
        """
        try:
            page_start_time = time.time()
            
            # Scroll to bottom
            self.scroll_to_bottom()
            
            # Wait for button to become clickable
            if not self.wait_for_button_clickable():
                logger.error("Button did not become clickable in time")
                return False
            
            # Click the button
            if not self.click_next_button():
                logger.error("Failed to click button")
                return False
            
            # Wait for new page to load (wait for URL change or new content)
            time.sleep(2)
            
            page_duration = time.time() - page_start_time
            self.total_wait_time += page_duration
            self.page_count += 1
            
            logger.info(
                f"Completed page {self.page_count} in {page_duration:.1f}s "
                f"(Total runtime: {self.total_wait_time:.0f}s)"
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error during navigation: {e}")
            return False
    
    def run(self):
        """Main loop - runs indefinitely navigating through pages."""
        logger.info("=" * 60)
        logger.info("Starting Page Navigator")
        logger.info(f"Target URL: {self.url}")
        logger.info(f"Button selector: {self.next_button_selector}")
        logger.info(f"Selector type: {self.selector_type}")
        logger.info("=" * 60)
        
        try:
            # Setup driver
            self.setup_driver()
            
            # Navigate to initial URL
            logger.info(f"Navigating to {self.url}")
            self.driver.get(self.url)
            time.sleep(3)  # Allow initial page load
            
            # Main loop - runs indefinitely
            consecutive_failures = 0
            max_consecutive_failures = 3
            
            while True:
                try:
                    logger.info(f"\n--- Processing page {self.page_count + 1} ---")
                    
                    success = self.navigate_to_next_page()
                    
                    if success:
                        consecutive_failures = 0
                    else:
                        consecutive_failures += 1
                        logger.warning(
                            f"Navigation failed (consecutive failures: {consecutive_failures})"
                        )
                        
                        if consecutive_failures >= max_consecutive_failures:
                            logger.error(
                                f"Reached {max_consecutive_failures} consecutive failures. "
                                "Stopping to prevent infinite loop."
                            )
                            break
                        
                        # Brief pause before retry
                        time.sleep(5)
                    
                except KeyboardInterrupt:
                    logger.info("Keyboard interrupt received. Shutting down...")
                    break
                    
                except WebDriverException as e:
                    logger.error(f"WebDriver error: {e}")
                    consecutive_failures += 1
                    
                    if consecutive_failures >= max_consecutive_failures:
                        logger.error("Too many WebDriver errors. Attempting to restart driver...")
                        try:
                            self.cleanup()
                            time.sleep(5)
                            self.setup_driver()
                            self.driver.get(self.url)
                            consecutive_failures = 0
                        except Exception as restart_error:
                            logger.error(f"Failed to restart driver: {restart_error}")
                            break
                    
                except Exception as e:
                    logger.error(f"Unexpected error: {e}", exc_info=True)
                    consecutive_failures += 1
                    
                    if consecutive_failures >= max_consecutive_failures:
                        logger.error("Too many consecutive errors. Stopping.")
                        break
                    
                    time.sleep(5)
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("\nCleaning up...")
        logger.info(f"Total pages processed: {self.page_count}")
        logger.info(f"Total runtime: {self.total_wait_time:.0f}s ({self.total_wait_time/60:.1f} minutes)")
        
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automated page navigator with dynamic timer support"
    )
    parser.add_argument(
        'url',
        help='Starting URL to navigate'
    )
    parser.add_argument(
        '--selector',
        required=True,
        help='CSS selector, XPath, or other selector for the next button'
    )
    parser.add_argument(
        '--selector-type',
        default='CSS',
        choices=['CSS', 'XPATH', 'ID', 'CLASS', 'NAME', 'TAG', 'LINK_TEXT', 'PARTIAL_LINK_TEXT'],
        help='Type of selector (default: CSS)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    parser.add_argument(
        '--check-interval',
        type=float,
        default=2.0,
        help='How often to check if button is clickable, in seconds (default: 2.0)'
    )
    parser.add_argument(
        '--max-wait',
        type=int,
        default=3600,
        help='Maximum time to wait per page in seconds (default: 3600 = 1 hour)'
    )
    
    args = parser.parse_args()
    
    navigator = PageNavigator(
        url=args.url,
        next_button_selector=args.selector,
        selector_type=args.selector_type,
        headless=args.headless,
        check_interval=args.check_interval,
        max_wait_per_page=args.max_wait
    )
    
    navigator.run()


if __name__ == '__main__':
    main()

