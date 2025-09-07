#!/usr/bin/env python3
"""
Simple test script for Trademark Search Web Application
Tests basic setup without Unicode characters for Windows compatibility
"""

import sys
import os

def main():
    print("=== Trademark Search Web Application - Basic Tests ===")
    print()
    
    # Test 1: Python version
    print("1. Testing Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   PASS: Python version is compatible")
        test1_pass = True
    else:
        print("   FAIL: Python 3.8+ required")
        test1_pass = False
    
    # Test 2: File structure
    print("\n2. Testing file structure...")
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'utils/scraper.py',
        'utils/excel_generator.py'
    ]
    
    test2_pass = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   PASS: {file_path}")
        else:
            print(f"   FAIL: {file_path} - Missing!")
            test2_pass = False
    
    # Test 3: Basic imports
    print("\n3. Testing basic Python modules...")
    basic_modules = ['threading', 'time', 'datetime', 'base64', 'json', 'os', 'uuid']
    test3_pass = True
    
    for module in basic_modules:
        try:
            __import__(module)
            print(f"   PASS: {module}")
        except ImportError:
            print(f"   FAIL: {module}")
            test3_pass = False
    
    # Test 4: Check templates
    print("\n4. Testing template files...")
    test4_pass = True
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Flask' in content or '{{' in content:
                print("   PASS: HTML template looks correct")
            else:
                print("   FAIL: HTML template may be incorrect")
                test4_pass = False
    except Exception as e:
        print(f"   FAIL: Cannot read template - {e}")
        test4_pass = False
    
    # Summary
    print("\n" + "=" * 50)
    total_tests = 4
    passed_tests = sum([test1_pass, test2_pass, test3_pass, test4_pass])
    print(f"Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\nSUCCESS: All basic tests passed!")
        print("\nNext steps to run the application:")
        print("1. Install dependencies:")
        print("   pip install flask selenium pillow openpyxl webdriver-manager")
        print("2. Run the application:")
        print("   python app.py")
        print("3. Open browser and go to:")
        print("   http://localhost:5000")
        return True
    else:
        print(f"\nWARNING: {total_tests - passed_tests} test(s) failed")
        print("Please check the issues above before proceeding.")
        return False

if __name__ == "__main__":
    main()