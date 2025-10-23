"""
Test script for Cipher V1 RBot
Verifies all components are working correctly
"""

import sys
import importlib
import json

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'pyautogui',
        'cv2',
        'numpy',
        'PIL',
        'win32gui',
        'keyboard',
        'threading',
        'logging'
    ]
    
    print("Testing module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_config():
    """Test if config file is valid"""
    print("\nTesting configuration file...")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✓ config.json is valid")
        return True
    except Exception as e:
        print(f"✗ config.json error - {e}")
        return False

def test_bot_class():
    """Test if bot class can be instantiated"""
    print("\nTesting bot class...")
    try:
        from cipher_bot import CipherBot
        bot = CipherBot()
        print("✓ CipherBot class instantiated successfully")
        return True
    except Exception as e:
        print(f"✗ CipherBot error - {e}")
        return False

def main():
    print("="*50)
    print("    CIPHER V1 RBOT - SYSTEM TEST")
    print("="*50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_config():
        tests_passed += 1
    
    if test_bot_class():
        tests_passed += 1
    
    print("\n" + "="*50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All systems ready! Your bot is ready to run!")
        print("\nTo start the bot:")
        print("1. Launch Roblox and join a game")
        print("2. Run: python cipher_bot.py")
        print("3. Or double-click launch_bot.bat")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Try running: pip install -r requirements.txt")
    
    print("="*50)

if __name__ == "__main__":
    main()