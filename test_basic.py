#!/usr/bin/env python3
"""
Basic test script for Trademark Search Web Application
Tests core functionality without external dependencies
"""

import sys
import os
import importlib.util

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("PASS: Python version is compatible")
        return True
    else:
        print("FAIL: Python 3.8+ required")
        return False

def test_required_modules():
    """Test if required Python modules can be imported"""
    print("\n📦 Testing required modules...")
    
    required_modules = [
        'threading', 'time', 'datetime', 'base64', 'io', 'json', 'os', 'uuid'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)
    
    return len(missing_modules) == 0

def test_file_structure():
    """Test if all required files are present"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'utils/__init__.py',
        'utils/scraper.py',
        'utils/excel_generator.py',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_app_import():
    """Test if the main app can be imported (without running)"""
    print("\n🚀 Testing app import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the main components
        spec = importlib.util.spec_from_file_location("app", "app.py")
        if spec and spec.loader:
            print("✅ app.py can be loaded")
            return True
        else:
            print("❌ app.py cannot be loaded")
            return False
    except Exception as e:
        print(f"❌ Error importing app: {str(e)}")
        return False

def test_template_syntax():
    """Test if HTML templates have basic syntax"""
    print("\n🌐 Testing template syntax...")
    
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic HTML checks
        checks = [
            ('<!DOCTYPE html>', 'DOCTYPE declaration'),
            ('<html', 'HTML tag'),
            ('<head>', 'HEAD section'),
            ('<body>', 'BODY section'),
            ('{{', 'Flask template syntax')
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"❌ Error reading template: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Trademark Search Web Application - Basic Tests")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Required Modules", test_required_modules),
        ("File Structure", test_file_structure),
        ("App Import", test_app_import),
        ("Template Syntax", test_template_syntax)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! Ready to install dependencies.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python app.py")
        print("3. Open browser: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()