"""
Screen Capture Utility
Captures game window screenshots efficiently
"""

import numpy as np
import cv2
import mss
import win32gui
from PIL import Image


class ScreenCapture:
    """Handles screen capture of the game window - HIGH FPS VERSION"""
    
    def __init__(self, config=None):
        self.config = config
        self.sct = None
        self.window_handle = None
        self.game_window_name = "Roblox"
        
        if config and hasattr(config, 'GAME_WINDOW_NAME'):
            self.game_window_name = config.GAME_WINDOW_NAME
        
        # Default capture size
        self.capture_width = 800
        self.capture_height = 600
        
        if config:
            if hasattr(config, 'CAPTURE_WIDTH'):
                self.capture_width = config.CAPTURE_WIDTH
            if hasattr(config, 'CAPTURE_HEIGHT'):
                self.capture_height = config.CAPTURE_HEIGHT
        
        # Find game window
        self._find_window()
    
    def _get_sct(self):
        """Get mss instance (thread-safe)"""
        if self.sct is None:
            self.sct = mss.mss()
        return self.sct
    
    def _find_window(self):
        """Find the game window handle"""
        self.window_handle = win32gui.FindWindow(None, self.game_window_name)
        if not self.window_handle:
            print(f"[WARNING] Could not find window: {self.game_window_name}")
    
    def capture(self):
        """
        Capture current game window
        Returns: numpy array of screenshot (BGR format)
        """
        if not self.window_handle:
            self._find_window()
            if not self.window_handle:
                return None
        
        try:
            # Get window position
            left, top, right, bottom = win32gui.GetWindowRect(self.window_handle)
            width = right - left
            height = bottom - top
            
            # Capture using mss (fastest method)
            monitor = {
                "top": top,
                "left": left,
                "width": width,
                "height": height
            }
            
            sct = self._get_sct()
            screenshot = sct.grab(monitor)
            
            # Convert to numpy array
            frame = np.array(screenshot)
            
            # Convert BGRA to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # Resize to target resolution
            if width != self.capture_width or height != self.capture_height:
                frame = cv2.resize(frame, (self.capture_width, self.capture_height))
            
            return frame
            
        except Exception as e:
            print(f"[ERROR] Screen capture failed: {e}")
            return None
    
    def capture_region(self, x, y, w, h):
        """Capture specific region of the window"""
        if not self.window_handle:
            return None
        
        try:
            left, top, right, bottom = win32gui.GetWindowRect(self.window_handle)
            
            monitor = {
                "top": top + y,
                "left": left + x,
                "width": w,
                "height": h
            }
            
            sct = self._get_sct()
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            return frame
            
        except Exception as e:
            print(f"[ERROR] Region capture failed: {e}")
            return None
    
    def close(self):
        """Cleanup resources"""
        if self.sct:
            try:
                self.sct.close()
            except:
                pass
            self.sct = None
