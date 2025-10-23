"""
Simple Movement Test for Cipher Bot
Tests if the bot can send keyboard commands properly
"""

import time
import pyautogui
import win32gui
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def find_roblox_window():
    """Find Roblox window"""
    def enum_windows_callback(hwnd, windows):
        try:
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "Roblox" in window_title and "Studio" not in window_title:
                    windows.append((hwnd, window_title))
        except Exception:
            pass
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows[0] if windows else None

def test_movement():
    """Test basic movement commands"""
    logger.info("=== MOVEMENT TEST ===")
    
    # Find Roblox window
    window_info = find_roblox_window()
    if not window_info:
        logger.error("No Roblox window found!")
        return False
    
    hwnd, title = window_info
    logger.info(f"Found window: {title}")
    
    # Focus window
    try:
        win32gui.SetForegroundWindow(hwnd)
        logger.info("Focused Roblox window")
    except Exception as e:
        logger.warning(f"Could not focus window: {e}")
    
    time.sleep(2)
    
    # Test movement sequence
    movements = [
        ("W (Forward)", 'w', 1.0),
        ("A (Left)", 'a', 0.5),
        ("S (Backward)", 's', 1.0),
        ("D (Right)", 'd', 0.5),
        ("W (Forward)", 'w', 1.0)
    ]
    
    logger.info("Starting movement test in 3 seconds...")
    time.sleep(3)
    
    for description, key, duration in movements:
        logger.info(f"Testing {description} for {duration} seconds")
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        time.sleep(0.5)  # Brief pause between movements
    
    logger.info("Movement test complete!")
    logger.info("Did you see any movement in Roblox?")
    return True

def main():
    print("="*50)
    print("    CIPHER BOT - MOVEMENT TEST")
    print("="*50)
    print()
    print("This will test if the bot can send movement commands.")
    print()
    print("Instructions:")
    print("1. Make sure Roblox is focused and visible")
    print("2. If in a game, make sure your character can move")
    print("3. Watch for WASD movement commands")
    print()
    
    input("Press Enter to start the movement test...")
    
    if test_movement():
        print("\nTest completed! Check the logs above.")
        print("If you didn't see movement, the issue might be:")
        print("- Roblox isn't focused properly")
        print("- You're in a menu instead of a game")
        print("- Character is stuck or can't move")
    else:
        print("\nTest failed - could not find Roblox window")

if __name__ == "__main__":
    main()