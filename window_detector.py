"""
Roblox Window Detector - Debug Tool
Helps identify Roblox windows and test window detection
"""

import win32gui
import win32con
import time

def list_all_windows():
    """List all visible windows"""
    def enum_windows_callback(hwnd, windows):
        try:
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:  # Only show windows with titles
                    class_name = win32gui.GetClassName(hwnd)
                    windows.append((hwnd, window_title, class_name))
        except Exception:
            pass
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def find_roblox_windows():
    """Find all Roblox-related windows"""
    windows = list_all_windows()
    roblox_windows = []
    
    for hwnd, title, class_name in windows:
        if "roblox" in title.lower():
            try:
                rect = win32gui.GetWindowRect(hwnd)
                is_valid = win32gui.IsWindow(hwnd)
                roblox_windows.append((hwnd, title, class_name, rect, is_valid))
            except Exception as e:
                roblox_windows.append((hwnd, title, class_name, None, False))
    
    return roblox_windows

def main():
    print("="*60)
    print("          ROBLOX WINDOW DETECTOR")
    print("="*60)
    print()
    
    print("Searching for Roblox windows...")
    roblox_windows = find_roblox_windows()
    
    if not roblox_windows:
        print("❌ No Roblox windows found!")
        print()
        print("Troubleshooting:")
        print("1. Make sure Roblox is running")
        print("2. Make sure you're in a game (not just launcher)")
        print("3. Make sure the window is visible (not minimized)")
        print()
        print("Here are ALL visible windows containing text:")
        all_windows = list_all_windows()
        for i, (hwnd, title, class_name) in enumerate(all_windows[:20]):  # Show first 20
            print(f"  {i+1:2d}. {title[:50]}")
        if len(all_windows) > 20:
            print(f"  ... and {len(all_windows)-20} more windows")
    else:
        print(f"✅ Found {len(roblox_windows)} Roblox window(s):")
        print()
        
        for i, (hwnd, title, class_name, rect, is_valid) in enumerate(roblox_windows):
            print(f"Window {i+1}:")
            print(f"  Handle: {hwnd}")
            print(f"  Title: {title}")
            print(f"  Class: {class_name}")
            print(f"  Valid: {is_valid}")
            if rect:
                print(f"  Position: {rect}")
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                print(f"  Size: {width}x{height}")
            else:
                print(f"  Position: Error getting rectangle")
            
            # Test if we can focus this window
            if is_valid:
                try:
                    print(f"  Focus Test: ", end="")
                    win32gui.SetForegroundWindow(hwnd)
                    print("✅ SUCCESS")
                except Exception as e:
                    print(f"❌ FAILED - {e}")
            print()
        
        # Recommend the best window
        game_windows = [w for w in roblox_windows if "Studio" not in w[1] and len(w[1]) > 6]
        if game_windows:
            best_window = game_windows[0]
            print(f"🎯 RECOMMENDED: '{best_window[1]}'")
            print("   This appears to be a Roblox game window (not Studio)")
        else:
            print("⚠️  No obvious game windows found. Make sure you're in a Roblox game!")
    
    print()
    print("="*60)

if __name__ == "__main__":
    main()