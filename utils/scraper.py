# -*- coding: utf-8 -*-
"""
Selenium scraper for Indian Trademark Registry
Maintains exact same functionality and element IDs as desktop version
"""

import time
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService

class TrademarkScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.search_results = []
    
    def initialize_browser(self, wordmark, trademark_class, filter_type):
        """Initialize browser and navigate to search page - EXACT same logic as desktop version"""
        try:
            # Setup Chrome - SAME options as desktop version
            options = Options()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # For headless deployment (can be enabled via environment variable)
            import os
            if os.environ.get('HEADLESS', 'false').lower() == 'true':
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--remote-debugging-port=9222")
            
            # Use system-installed ChromeDriver only
            try:
                # Use system chromedriver (installed in Dockerfile)
                service = ChromeService("/usr/bin/chromedriver")
                self.driver = webdriver.Chrome(service=service, options=options)
                print("SUCCESS: Using system ChromeDriver")
            except Exception as e:
                print(f"FAILED to use system ChromeDriver: {e}")
                try:
                    # Fallback: let Chrome find its own driver  
                    self.driver = webdriver.Chrome(options=options)
                    print("SUCCESS: Using Chrome's built-in driver")
                except Exception as e2:
                    print(f"FAILED Chrome built-in driver: {e2}")
                    raise Exception(f"ChromeDriver initialization failed: {e} | {e2}")
            
            self.wait = WebDriverWait(self.driver, 20)
            
            # Navigate to website - SAME URL as desktop version
            self.driver.get("https://tmrsearch.ipindia.gov.in/tmrpublicsearch/frmmain.aspx")
            time.sleep(3)
            
            # Fill search form - EXACT same element IDs as desktop version
            
            # Select search type - SAME element ID
            search_type = Select(self.driver.find_element(By.ID, "ContentPlaceHolder1_DDLSearchType"))
            search_type.select_by_value("WM")
            time.sleep(0.5)
            
            # Select filter - SAME logic as desktop version
            filter_map = {"Start With": "0", "Contains": "1", "Match With": "2"}
            filter_select = Select(self.driver.find_element(By.ID, "ContentPlaceHolder1_DDLFilter"))
            filter_select.select_by_value(filter_map[filter_type])
            time.sleep(0.5)
            
            # Enter wordmark - SAME element ID
            wordmark_input = self.driver.find_element(By.ID, "ContentPlaceHolder1_TBWordmark")
            wordmark_input.clear()
            wordmark_input.send_keys(wordmark)
            time.sleep(0.5)
            
            # Enter class - SAME element ID
            class_input = self.driver.find_element(By.ID, "ContentPlaceHolder1_TBClass")
            class_input.clear()
            class_input.send_keys(trademark_class)
            time.sleep(0.5)
            
            # Get CAPTCHA image - SAME element ID as desktop version
            captcha_element = self.driver.find_element(By.ID, "ContentPlaceHolder1_ImageCaptcha")
            
            # Take screenshot of CAPTCHA - SAME method as desktop version
            captcha_screenshot = captcha_element.screenshot_as_png
            
            # Convert to base64 for web display
            captcha_base64 = base64.b64encode(captcha_screenshot).decode('utf-8')
            
            return captcha_base64
            
        except Exception as e:
            self.cleanup()
            raise Exception(f"Browser initialization error: {str(e)}")
    
    def submit_search(self, captcha_text):
        """Submit search with CAPTCHA - EXACT same logic as desktop version"""
        try:
            # Enter CAPTCHA - SAME element ID
            captcha_input = self.driver.find_element(By.ID, "ContentPlaceHolder1_captcha1")
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            time.sleep(0.5)
            
            # Click search button - SAME element ID and method
            search_button = self.driver.find_element(By.ID, "ContentPlaceHolder1_BtnSearch")
            self.driver.execute_script("arguments[0].click();", search_button)
            
            # Wait for results - SAME logic
            time.sleep(3)
            
            # Check if we got results - SAME element ID
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_MGVSearchResult")))
                return True
            except TimeoutException:
                raise Exception("No results found or wrong CAPTCHA. Please try again.")
                
        except Exception as e:
            raise Exception(f"Search submission error: {str(e)}")
    
    def extract_results(self, progress_callback=None):
        """Extract trademark results - EXACT same logic as desktop version"""
        try:
            self.search_results = []
            
            # Try to load more results - SAME logic as desktop version
            for i in range(5):  # Try 5 times to load more
                try:
                    load_more = self.driver.find_element(By.LINK_TEXT, "Load More...")
                    if load_more.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(2)
                        if progress_callback:
                            progress_callback(i, 5, f"Loading more results ({i+1}/5)...")
                except:
                    break
            
            # Get results grid - SAME element ID
            grid = self.driver.find_element(By.ID, "ContentPlaceHolder1_MGVSearchResult")
            rows = grid.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header
            
            total_rows = len(rows)
            if progress_callback:
                progress_callback(0, total_rows, f"Processing {total_rows} results...")
            
            for idx, row in enumerate(rows):
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:
                        result = {}
                        
                        # Extract text data - EXACT same XPath selectors as desktop version
                        text_cell = cells[1]
                        
                        # Wordmark - SAME XPath
                        try:
                            wordmark = text_cell.find_element(By.XPATH, ".//span[contains(@id, 'lblsimiliarmark')]").text
                            result["Wordmark"] = wordmark
                        except:
                            result["Wordmark"] = ""
                        
                        # Proprietor - SAME XPath
                        try:
                            proprietor = text_cell.find_element(By.XPATH, ".//span[contains(@id, 'LblVProprietorName')]").text
                            result["Proprietor"] = proprietor
                        except:
                            result["Proprietor"] = ""
                        
                        # Application Number - SAME XPath
                        try:
                            app_num = text_cell.find_element(By.XPATH, ".//span[contains(@id, 'lblapplicationnumber')]").text
                            result["Application_Number"] = app_num
                        except:
                            result["Application_Number"] = ""
                        
                        # Class - SAME XPath
                        try:
                            class_text = text_cell.find_element(By.XPATH, ".//span[contains(@id, 'lblsearchclass')]").text
                            result["Class"] = class_text
                        except:
                            result["Class"] = ""
                        
                        # Status - SAME XPath
                        try:
                            status = text_cell.find_element(By.XPATH, ".//span[contains(@id, 'Label6')]").text
                            result["Status"] = status
                        except:
                            result["Status"] = ""
                        
                        # Extract image - EXACT same logic as desktop version
                        try:
                            image_cell = cells[2]
                            image_elem = image_cell.find_element(By.TAG_NAME, "img")
                            image_src = image_elem.get_attribute("src")
                            
                            if image_src and image_src.startswith("data:image"):
                                # Extract base64 data - SAME method
                                image_data = image_src.split(",")[1]
                                image_bytes = base64.b64decode(image_data)
                                
                                # Store image bytes directly in the result - SAME as desktop
                                result["Image_Data"] = image_bytes
                            else:
                                result["Image_Data"] = None
                        except:
                            result["Image_Data"] = None
                        
                        # Add search metadata - SAME as desktop version
                        result["Search_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        self.search_results.append(result)
                        
                        # Progress callback
                        if progress_callback:
                            progress_callback(idx + 1, total_rows, f"Processed {idx + 1}/{total_rows} results")
                        
                except Exception as e:
                    print(f"Error extracting row {idx}: {str(e)}")
                    continue
            
            return self.search_results
            
        except Exception as e:
            raise Exception(f"Results extraction error: {str(e)}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
        except:
            pass