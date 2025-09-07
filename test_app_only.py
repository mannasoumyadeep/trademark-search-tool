#!/usr/bin/env python3
"""
Test Flask application without Selenium (UI testing only)
"""

def test_flask_app():
    print("=== Flask Application Test ===")
    
    try:
        # Import Flask app
        from app import app
        print("1. PASS: Flask app imported successfully")
        
        # Test app configuration
        app.config['TESTING'] = True
        client = app.test_client()
        print("2. PASS: Test client created")
        
        # Test main route
        response = client.get('/')
        print(f"3. Main page status: {response.status_code}")
        if response.status_code == 200:
            print("   PASS: Main page loads")
        else:
            print("   FAIL: Main page error")
            return False
        
        # Test health endpoint
        response = client.get('/health')
        print(f"4. Health check status: {response.status_code}")
        if response.status_code == 200:
            print("   PASS: Health check works")
        else:
            print("   FAIL: Health check error")
        
        # Test HTML content
        response = client.get('/')
        if b'Trademark Search' in response.data:
            print("5. PASS: Page contains expected content")
        else:
            print("5. FAIL: Page content issue")
            return False
        
        print("\nSUCCESS: Flask application is working correctly!")
        return True
        
    except Exception as e:
        print(f"FAIL: {e}")
        return False

def show_manual_test_instructions():
    print("\n=== Manual Testing Instructions ===")
    print()
    print("To test the full application manually:")
    print()
    print("1. Start the application:")
    print("   python app.py")
    print()
    print("2. Open your browser and go to:")
    print("   http://localhost:5000")
    print()
    print("3. You should see:")
    print("   - A professional-looking interface")
    print("   - Search form with wordmark, class, filter fields")
    print("   - 'Start Search' button")
    print()
    print("4. To test search functionality:")
    print("   a) Enter a wordmark (e.g., 'Apple')")
    print("   b) Optionally enter a class (e.g., '09')")
    print("   c) Click 'Start Search'")
    print("   d) Wait for CAPTCHA to load")
    print("   e) Enter CAPTCHA text")
    print("   f) Click 'Submit Search'")
    print("   g) Wait for results and export to Excel")
    print()
    print("5. Expected behavior:")
    print("   - Same search results as your desktop version")
    print("   - Images embedded in Excel file")
    print("   - 60-point row heights in Excel")
    print()
    print("Note: Chrome/Selenium functionality requires internet connection")
    print("and Google Chrome browser installed.")

if __name__ == "__main__":
    if test_flask_app():
        show_manual_test_instructions()
    else:
        print("Please check the error messages above.")