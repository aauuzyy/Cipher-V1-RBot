"""
Input Controller - Direct input for Roblox
Uses ctypes for proper key sending that works in games
"""

import ctypes
import time
from ctypes import wintypes

# Windows constants
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

# Virtual key codes
VK_CODE = {
    'w': 0x57,
    'a': 0x41,
    's': 0x53,
    'd': 0x44,
    'space': 0x20,
    'shift': 0x10,
    'ctrl': 0x11,
    'enter': 0x0D,
    'esc': 0x1B,
    '/': 0xBF,
    'left': 0x25,   # Arrow left
    'right': 0x27,  # Arrow right
    'up': 0x26,     # Arrow up
    'down': 0x28,   # Arrow down
}

# Scan codes (more reliable for games)
SCAN_CODE = {
    'w': 0x11,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'space': 0x39,
    'shift': 0x2A,
    'ctrl': 0x1D,
    'enter': 0x1C,
    'esc': 0x01,
    '/': 0x35,
    'left': 0x4B,   # Arrow left scan code (correct)
    'right': 0x4D,  # Arrow right scan code (correct)
    'up': 0x48,     # Arrow up scan code (correct)
    'down': 0x50,   # Arrow down scan code (correct)
}

# Define structures
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", _INPUT_UNION)
    ]


class InputController:
    """High-level input controller using direct input"""
    
    def __init__(self, config=None):
        self.config = config
        self.pressed_keys = set()
        
    def press_key(self, key):
        """Press a key down (using scan code for games)"""
        key = key.lower()
        
        if key in self.pressed_keys:
            return
        
        scan_code = SCAN_CODE.get(key, 0)
        if scan_code == 0:
            return
        
        # Create input structure
        extra = ctypes.c_ulong(0)
        ii_ = _INPUT_UNION()
        ii_.ki = KEYBDINPUT(
            wVk=0,  # Use 0 for scan code input
            wScan=scan_code,
            dwFlags=KEYEVENTF_SCANCODE,
            time=0,
            dwExtraInfo=ctypes.pointer(extra)
        )
        
        x = INPUT(type=INPUT_KEYBOARD, union=ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        
        self.pressed_keys.add(key)
    
    def release_key(self, key):
        """Release a key"""
        key = key.lower()
        
        if key not in self.pressed_keys:
            return
        
        scan_code = SCAN_CODE.get(key, 0)
        if scan_code == 0:
            return
        
        # Create input structure for key release
        extra = ctypes.c_ulong(0)
        ii_ = _INPUT_UNION()
        ii_.ki = KEYBDINPUT(
            wVk=0,
            wScan=scan_code,
            dwFlags=KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP,
            time=0,
            dwExtraInfo=ctypes.pointer(extra)
        )
        
        x = INPUT(type=INPUT_KEYBOARD, union=ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        
        self.pressed_keys.discard(key)
    
    def tap_key(self, key, duration=0.05):
        """Tap a key (press and release)"""
        self.press_key(key)
        time.sleep(duration)
        self.release_key(key)
    
    def hold_key(self, key, duration):
        """Hold a key for specified duration"""
        self.press_key(key)
        time.sleep(duration)
        self.release_key(key)
    
    def release_all(self):
        """Release all currently pressed keys"""
        keys_to_release = list(self.pressed_keys)
        for key in keys_to_release:
            self.release_key(key)
    
    def move_mouse(self, dx, dy):
        """Move mouse relative (for camera control)"""
        extra = ctypes.c_ulong(0)
        ii_ = _INPUT_UNION()
        ii_.mi = MOUSEINPUT(
            dx=dx,
            dy=dy,
            mouseData=0,
            dwFlags=0x0001,  # MOUSEEVENTF_MOVE
            time=0,
            dwExtraInfo=ctypes.pointer(extra)
        )
        
        x = INPUT(type=0, union=ii_)  # 0 = INPUT_MOUSE
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    def type_text(self, text):
        """Type text character by character"""
        for char in text:
            # Press
            vk = VK_CODE.get(char.lower(), ord(char.upper()))
            scan = SCAN_CODE.get(char.lower(), 0)
            
            extra = ctypes.c_ulong(0)
            ii_ = _INPUT_UNION()
            ii_.ki = KEYBDINPUT(
                wVk=vk,
                wScan=scan,
                dwFlags=0,
                time=0,
                dwExtraInfo=ctypes.pointer(extra)
            )
            x = INPUT(type=INPUT_KEYBOARD, union=ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            
            time.sleep(0.01)
            
            # Release
            ii_.ki.dwFlags = KEYEVENTF_KEYUP
            x = INPUT(type=INPUT_KEYBOARD, union=ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            
            time.sleep(0.02)
