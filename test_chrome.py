#!/usr/bin/env python3
"""
Test Chrome WebDriver availability
"""

def test_chrome():
    print("Testing Chrome WebDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service as ChromeService
        
        print("1. PASS: Selenium imports successful")
        
        # Test Chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        print("2. PASS: Chrome options configured")
        
        # Test ChromeDriverManager
        try:
            service = ChromeService(ChromeDriverManager().install())
            print("3. PASS: ChromeDriver downloaded/found")
        except Exception as e:
            print(f"3. FAIL: ChromeDriver issue - {e}")
            return False
        
        # Test browser initialization (quick test)
        try:
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("about:blank")
            print("4. PASS: Chrome browser can be started")
            driver.quit()
            print("5. PASS: Chrome browser closed successfully")
        except Exception as e:
            print(f"4. FAIL: Chrome browser error - {e}")
            return False
            
        return True
        
    except ImportError as e:
        print(f"FAIL: Import error - {e}")
        return False
    except Exception as e:
        print(f"FAIL: General error - {e}")
        return False

if __name__ == "__main__":
    print("=== Chrome WebDriver Test ===")
    
    if test_chrome():
        print("\nSUCCESS: Chrome WebDriver is working!")
        print("The application should be able to access trademark website.")
    else:
        print("\nWARNING: Chrome WebDriver has issues.")
        print("You may need to install Google Chrome browser.")
    
    print("\nNext: Run 'python app.py' to start the web application")