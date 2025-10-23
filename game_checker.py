"""
Roblox Game Checker
Helps determine if you're in a Roblox game or just the launcher
"""

import win32gui
import time

def check_roblox_status():
    """Check if we're in a game or launcher"""
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
    
    if not windows:
        return "❌ No Roblox windows found"
    
    results = []
    for hwnd, title in windows:
        if title.strip() == "Roblox":
            status = "🏠 LAUNCHER - No character to control"
            recommendation = "Join a game first!"
        else:
            status = "🎮 GAME - Ready for bot!"
            recommendation = "Perfect for bot usage!"
        
        results.append(f"Window: '{title}'\nStatus: {status}\nRecommendation: {recommendation}")
    
    return "\n\n".join(results)

def main():
    print("="*60)
    print("          ROBLOX GAME CHECKER")
    print("="*60)
    print()
    print("This tool helps you check if you're ready to use the bot.")
    print()
    
    while True:
        print("Current Roblox Status:")
        print("-" * 40)
        print(check_roblox_status())
        print("-" * 40)
        print()
        print("Options:")
        print("1. Press Enter to refresh")
        print("2. Type 'q' to quit")
        print("3. Run 'python cipher_bot.py' when you see 'GAME' status")
        print()
        
        choice = input("Your choice: ").strip().lower()
        if choice == 'q':
            break
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()