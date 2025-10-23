"""
Cipher V1 RBot - Advanced Roblox Bot
A sophisticated bot that walks around, avoids walls, and shares facts in Roblox games.
"""

import time
import random
import threading
import logging
from typing import Tuple, List, Optional
from pathlib import Path
import sys

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab
import win32gui
import win32con
import win32api
import keyboard
import json

# Import our direct input controller
from utils.input_controller import InputController

# Configure logging with UTF-8 encoding to handle emojis
import sys
import io

# Set UTF-8 encoding for console output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cipher_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class CipherBot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.bot_active = False  # New state for F1/F2 control
        self.roblox_window = None
        self.window_rect = None
        
        # Initialize direct input controller (WORKS WITH ROBLOX!)
        self.input_controller = InputController()
        self.logger.info("✓ Direct input controller initialized")
        
        # Load configuration
        self.config = self.load_config()
        
        # Movement settings from config
        self.movement_speed = self.config.get('movement', {}).get('speed', 0.1)
        self.turn_angle = self.config.get('movement', {}).get('turn_angle', 30)
        self.movement_duration = self.config.get('movement', {}).get('movement_duration', 2.0)
        self.wall_detection_threshold = self.config.get('movement', {}).get('wall_detection_threshold', 50)
        
        # Chat settings from config
        self.fact_interval = self.config.get('chat', {}).get('fact_interval', 30)
        self.last_fact_time = 0
        
        # Orange ball tracking settings
        self.BALL_COLOR_LOWER = np.array([5, 100, 100])   # Orange HSV lower
        self.BALL_COLOR_UPPER = np.array([25, 255, 255])  # Orange HSV upper
        self.MIN_BALL_AREA = 200
        self.MAX_BALL_AREA = 50000
        self.last_ball_pos = None
        
        # Initialize PyAutoGUI settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Setup hotkeys
        self.setup_hotkeys()
        
        self.logger.info("Cipher Bot initialized with hotkey controls (F1=Start, F2=Stop)")
        self.logger.info("🟠 Orange ball tracking enabled!")
    
    def load_config(self) -> dict:
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load config.json: {e}. Using defaults.")
            return {}
    
    def setup_hotkeys(self):
        """Setup F1 and F2 hotkeys for bot control"""
        try:
            keyboard.add_hotkey('f1', self.start_bot_hotkey)
            keyboard.add_hotkey('f2', self.stop_bot_hotkey)
            self.logger.info("Hotkeys registered: F1 = Start Bot, F2 = Stop Bot")
        except Exception as e:
            self.logger.error(f"Failed to setup hotkeys: {e}")
    
    def start_bot_hotkey(self):
        """Start the bot via F1 hotkey"""
        if not self.bot_active and self.roblox_window:
            self.bot_active = True
            self.last_fact_time = time.time()
            self.logger.info("🟢 Bot STARTED via F1 hotkey!")
            # NO CHAT MESSAGES
    
    def stop_bot_hotkey(self):
        """Stop the bot via F2 hotkey"""
        if self.bot_active:
            self.bot_active = False
            # Release all held keys
            self.input_controller.release_all()
            self.logger.info("🔴 Bot STOPPED via F2 hotkey!")
            # NO CHAT MESSAGES
    
    def find_roblox_window(self) -> bool:
        """Find and focus the Roblox window"""
        def enum_windows_callback(hwnd, windows):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "Roblox" in window_title and "Studio" not in window_title:
                        # Accept any Roblox window (including just "Roblox")
                        windows.append((hwnd, window_title))
            except Exception:
                pass  # Skip windows that cause errors
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        self.logger.info(f"Window detection found {len(windows)} Roblox windows")
        
        if not windows:
            self.logger.error("No Roblox windows found!")
            self.logger.error("Please make sure:")
            self.logger.error("1. Roblox is running (not just the launcher)")
            self.logger.error("2. You're in a game (not just the main menu)")
            self.logger.error("3. Roblox Studio is NOT what's running")
            self.logger.error("4. Try running: python window_detector.py")
            return False
        
        # Filter for actual game windows (not just "Roblox" launcher)
        game_windows = []
        launcher_windows = []
        
        for hwnd, title in windows:
            if title.strip() == "Roblox":
                launcher_windows.append((hwnd, title))
            else:
                game_windows.append((hwnd, title))
        
        # Show all found windows for debugging
        self.logger.info("Found Roblox windows:")
        for i, (hwnd, title) in enumerate(windows):
            window_type = "GAME" if title.strip() != "Roblox" else "LAUNCHER"
            self.logger.info(f"  {i+1}. [{window_type}] {title}")
        
        # Prefer game windows over launcher
        if game_windows:
            selected_window = game_windows[0]
            self.logger.info("SUCCESS: Using game window")
        elif launcher_windows:
            selected_window = launcher_windows[0]
            self.logger.warning("WARNING: Only found launcher window - please join a game!")
            self.logger.warning("The bot may not work properly until you're in a game.")
        else:
            self.logger.error("No suitable Roblox windows found")
            return False
        
        # Select the chosen window
        self.roblox_window = selected_window[0]
        window_title = selected_window[1]
        self.logger.info(f"Using window: {window_title}")
        
        try:
            # Validate the window handle
            if not win32gui.IsWindow(self.roblox_window):
                self.logger.error("Invalid window handle!")
                return False
            
            # Get window position and size
            self.window_rect = win32gui.GetWindowRect(self.roblox_window)
            self.logger.info(f"Window position: {self.window_rect}")
            
            # Try to focus the window with error handling
            try:
                # Alternative focusing method
                import ctypes
                from ctypes import wintypes
                
                # Try multiple focus methods
                success = False
                
                # Method 1: Standard SetForegroundWindow
                try:
                    win32gui.SetForegroundWindow(self.roblox_window)
                    success = True
                    self.logger.info("Successfully focused window (method 1)")
                except:
                    pass
                
                # Method 2: ShowWindow + SetFocus
                if not success:
                    try:
                        win32gui.ShowWindow(self.roblox_window, win32con.SW_RESTORE)
                        win32gui.SetFocus(self.roblox_window)
                        success = True
                        self.logger.info("Successfully focused window (method 2)")
                    except:
                        pass
                
                # Method 3: Alt+Tab simulation to bring window forward
                if not success:
                    try:
                        # Simulate Alt+Tab to the window
                        import pyautogui
                        pyautogui.keyDown('alt')
                        pyautogui.press('tab')
                        pyautogui.keyUp('alt')
                        time.sleep(0.5)
                        success = True
                        self.logger.info("Used Alt+Tab method for window focus")
                    except:
                        pass
                
                if not success:
                    self.logger.warning("Could not focus window automatically")
                    self.logger.info("Please manually click on the Roblox window to focus it")
                
            except Exception as e:
                self.logger.warning(f"Window focusing had issues: {e}")
                self.logger.info("Bot will still work if Roblox window is visible")
            
            time.sleep(1)
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up window: {e}")
            return False
    
    def take_screenshot(self) -> Optional[np.ndarray]:
        """Take a screenshot of the Roblox window"""
        try:
            if not self.window_rect:
                # Try to get window rect again if it's missing
                if self.roblox_window and win32gui.IsWindow(self.roblox_window):
                    self.window_rect = win32gui.GetWindowRect(self.roblox_window)
                else:
                    return None
            
            # Validate window rect
            left, top, right, bottom = self.window_rect
            if right <= left or bottom <= top:
                self.logger.warning("Invalid window dimensions")
                return None
            
            # Capture the window area
            screenshot = ImageGrab.grab(bbox=self.window_rect)
            
            # Check if screenshot is valid
            if screenshot.size[0] == 0 or screenshot.size[1] == 0:
                self.logger.warning("Screenshot has zero dimensions")
                return None
            
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
            
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            # Try to refresh window info
            if self.roblox_window:
                try:
                    if win32gui.IsWindow(self.roblox_window):
                        self.window_rect = win32gui.GetWindowRect(self.roblox_window)
                    else:
                        self.logger.warning("Roblox window no longer exists")
                        self.roblox_window = None
                        self.window_rect = None
                except:
                    pass
            return None

    def ensure_roblox_focused(self):
        """Ensure Roblox window is focused before sending keys"""
        if not self.roblox_window:
            return False
        
        try:
            # Check if window still exists
            if not win32gui.IsWindow(self.roblox_window):
                self.logger.warning("Roblox window no longer exists, trying to re-detect...")
                return self.re_detect_window()
            
            # Get current foreground window
            current_fg = win32gui.GetForegroundWindow()
            
            # If Roblox is not in foreground, try to focus it
            if current_fg != self.roblox_window:
                self.logger.debug("Focusing Roblox window...")
                
                # Try multiple methods to focus the window
                try:
                    # Method 1: Standard SetForegroundWindow
                    win32gui.SetForegroundWindow(self.roblox_window)
                except:
                    try:
                        # Method 2: ShowWindow then SetForegroundWindow
                        win32gui.ShowWindow(self.roblox_window, win32con.SW_RESTORE)
                        time.sleep(0.1)
                        win32gui.SetForegroundWindow(self.roblox_window)
                    except:
                        try:
                            # Method 3: BringWindowToTop
                            win32gui.BringWindowToTop(self.roblox_window)
                        except:
                            self.logger.warning("Could not focus Roblox window")
                            return False
                
                # Small delay to ensure focus is set
                time.sleep(0.2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error focusing Roblox window: {e}")
            return False
    
    def check_window_valid(self) -> bool:
        """Check if the current window is still valid"""
        if not self.roblox_window:
            return False
        
        try:
            return win32gui.IsWindow(self.roblox_window) and win32gui.IsWindowVisible(self.roblox_window)
        except:
            return False
    
    def re_detect_window(self) -> bool:
        """Try to re-detect the Roblox window if it was lost"""
        self.logger.info("Attempting to re-detect Roblox window...")
        old_window = self.roblox_window
        
        if self.find_roblox_window():
            if old_window != self.roblox_window:
                self.logger.info("Successfully found new Roblox window")
            return True
        else:
            self.logger.warning("Could not re-detect Roblox window")
            return False
    
    def detect_walls(self, screenshot: np.ndarray) -> Tuple[bool, str]:
        """
        Detect walls or obstacles in front of the character
        Returns (is_wall_detected, direction_to_turn)
        """
        try:
            height, width = screenshot.shape[:2]
            
            # Define regions to check for walls (front, left, right)
            center_x, center_y = width // 2, height // 2
            
            # Front detection area
            front_region = screenshot[center_y-50:center_y+50, center_x-25:center_x+25]
            
            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(front_region, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Count edge pixels (indicating walls/obstacles)
            edge_count = np.sum(edges > 0)
            
            # If too many edges detected, we're likely facing a wall
            if edge_count > self.wall_detection_threshold:
                # Check left and right to determine best turn direction
                left_region = screenshot[center_y-50:center_y+50, center_x-100:center_x-50]
                right_region = screenshot[center_y-50:center_y+50, center_x+50:center_x+100]
                
                left_edges = np.sum(cv2.Canny(cv2.cvtColor(left_region, cv2.COLOR_BGR2GRAY), 50, 150) > 0)
                right_edges = np.sum(cv2.Canny(cv2.cvtColor(right_region, cv2.COLOR_BGR2GRAY), 50, 150) > 0)
                
                # Turn towards the direction with fewer obstacles
                turn_direction = "left" if right_edges > left_edges else "right"
                
                self.logger.info(f"Wall detected! Turning {turn_direction}")
                return True, turn_direction
            
            return False, ""
            
        except Exception as e:
            self.logger.error(f"Error in wall detection: {e}")
            return False, ""
    
    def find_orange_ball(self, frame):
        """
        Find orange ball in frame
        Returns: dict with ball info or None
        """
        if frame is None:
            return None
        
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create mask for orange color
            mask = cv2.inRange(hsv, self.BALL_COLOR_LOWER, self.BALL_COLOR_UPPER)
            
            # Clean up mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Find largest contour (likely the ball)
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Check if area is reasonable
            if area < self.MIN_BALL_AREA or area > self.MAX_BALL_AREA:
                return None
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Calculate center
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Store last position
            self.last_ball_pos = (center_x, center_y)
            
            return {
                'center': (center_x, center_y),
                'bbox': (x, y, w, h),
                'area': area,
                'size': max(w, h)
            }
        except Exception as e:
            self.logger.error(f"Error finding orange ball: {e}")
            return None
    
    def send_key_to_window(self, key_code, duration=None):
        """Send key directly to Roblox window using Windows API"""
        if not self.roblox_window:
            return False
        
        try:
            # Send key down message
            win32api.PostMessage(self.roblox_window, win32con.WM_KEYDOWN, key_code, 0)
            
            if duration:
                time.sleep(duration)
            
            # Send key up message
            win32api.PostMessage(self.roblox_window, win32con.WM_KEYUP, key_code, 0)
            return True
        except Exception as e:
            self.logger.error(f"Error sending key to window: {e}")
            return False

    def move_forward(self, duration: float = None):
        """Move the character forward using DIRECT INPUT"""
        if duration is None:
            duration = self.movement_duration
        
        self.logger.info(f"[DIRECT INPUT] Moving forward for {duration:.1f} seconds")
        
        # Ensure window is focused first
        self.ensure_roblox_focused()
        
        # Use direct input controller - THIS WORKS IN ROBLOX!
        self.input_controller.hold_key('w', duration)
    
    def turn_left(self, duration: float = 0.5):
        """Turn camera left using LEFT ARROW"""
        self.logger.info(f"[ARROW KEY] Turning camera left for {duration:.1f} seconds")
        
        # Ensure window is focused
        self.ensure_roblox_focused()
        
        # Use left arrow key to turn camera
        self.input_controller.hold_key('left', duration)
    
    def turn_right(self, duration: float = 0.5):
        """Turn camera right using RIGHT ARROW"""
        self.logger.info(f"[ARROW KEY] Turning camera right for {duration:.1f} seconds")
        
        # Ensure window is focused
        self.ensure_roblox_focused()
        
        # Use right arrow key to turn camera
        self.input_controller.hold_key('right', duration)
    
    def random_turn(self):
        """Make a random turn"""
        if random.choice([True, False]):
            self.turn_left(random.uniform(0.3, 0.8))
        else:
            self.turn_right(random.uniform(0.3, 0.8))
    
    def send_chat_message(self, message: str):
        """Send a message in the Roblox chat using DIRECT INPUT"""
        try:
            # Ensure window is focused
            self.ensure_roblox_focused()
            
            # Press '/' to open chat
            self.input_controller.tap_key('/')
            time.sleep(0.3)
            
            # Type the message
            self.input_controller.type_text(message)
            time.sleep(0.2)
            
            # Press Enter to send
            self.input_controller.tap_key('enter')
            time.sleep(0.5)
            
            self.logger.info(f"Sent message: {message}")
            
        except Exception as e:
            self.logger.error(f"Error sending chat message: {e}")
    
    def get_random_fact(self) -> str:
        """Get a random interesting fact"""
        facts = [
            "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
            "Fun fact: Octopuses have three hearts and blue blood!",
            "Amazing fact: A group of flamingos is called a 'flamboyance'!",
            "Cool fact: Bananas are berries, but strawberries aren't!",
            "Interesting: The shortest war in history lasted only 38-45 minutes between Britain and Zanzibar in 1896!",
            "Did you know? A single cloud can weigh more than a million pounds!",
            "Fun fact: Dolphins have names for each other - they use specific whistle signatures!",
            "Amazing: Your brain uses about 20% of your total energy despite being only 2% of your body weight!",
            "Cool fact: There are more possible games of chess than atoms in the observable universe!",
            "Interesting: Wombat poop is cube-shaped!",
            "Did you know? The heart of a blue whale is so large that a human could crawl through its arteries!",
            "Fun fact: Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid!",
            "Amazing: Butterflies taste with their feet!",
            "Cool fact: A day on Venus is longer than a year on Venus!",
            "Interesting: The immortal jellyfish can theoretically live forever by reverting to its juvenile state!"
        ]
        return random.choice(facts)
    
    def chat_facts_loop(self):
        """Background thread for sending facts - DISABLED"""
        # Chat disabled for now, will add facts later
        while self.running:
            time.sleep(1)
    
    def movement_loop(self):
        """Main movement loop - WALKS FORWARD AND FOLLOWS ORANGE"""
        while self.running:
            try:
                # Only move if bot is active
                if self.bot_active:
                    # Check if window is still valid
                    if not self.check_window_valid():
                        self.logger.warning("Roblox window lost, attempting to re-detect...")
                        if not self.re_detect_window():
                            self.logger.error("Cannot find Roblox window. Pausing bot...")
                            self.bot_active = False
                            time.sleep(5)
                            continue
                    
                    # Take screenshot for detection
                    screenshot = self.take_screenshot()
                    
                    if screenshot is not None:
                        # Look for orange ball FIRST
                        ball = self.find_orange_ball(screenshot)
                        
                        if ball:
                            # ORANGE BALL DETECTED - FOLLOW IT!
                            self.logger.info(f"🟠 TRACKING ORANGE! Area: {ball['area']}")
                            
                            height, width = screenshot.shape[:2]
                            screen_center_x = width // 2
                            ball_x, ball_y = ball['center']
                            
                            # Calculate offset from center
                            dx = ball_x - screen_center_x
                            
                            # Release any turning keys first
                            self.input_controller.release_key('left')
                            self.input_controller.release_key('right')
                            
                            # Turn camera to CENTER the ball (hold arrow keys)
                            if abs(dx) > 30:  # Dead zone - smaller for precision
                                if dx > 0:
                                    # Ball is to the RIGHT - hold RIGHT arrow
                                    self.input_controller.press_key('right')
                                    self.logger.info(f"  → Turning RIGHT (offset: {dx})")
                                else:
                                    # Ball is to the LEFT - hold LEFT arrow  
                                    self.input_controller.press_key('left')
                                    self.logger.info(f"  ← Turning LEFT (offset: {dx})")
                            else:
                                # Ball is centered! Release turn keys
                                self.input_controller.release_key('left')
                                self.input_controller.release_key('right')
                                self.logger.info(f"  ✓ CENTERED! Walking toward orange")
                            
                            # Always walk forward when tracking orange
                            self.input_controller.press_key('w')
                            time.sleep(0.02)  # Super fast tracking
                            
                        else:
                            # NO ORANGE - Wander and search
                            self.logger.info("🔍 No orange detected - wandering...")
                            
                            # Release turning keys
                            self.input_controller.release_key('left')
                            self.input_controller.release_key('right')
                            
                            # Keep walking forward
                            self.input_controller.press_key('w')
                            
                            # Check for walls
                            wall_detected, turn_direction = self.detect_walls(screenshot)
                            
                            if wall_detected:
                                # Release W and turn away from wall
                                self.input_controller.release_key('w')
                                self.logger.info(f"Wall ahead! Turning {turn_direction}")
                                
                                if turn_direction == "left":
                                    self.input_controller.hold_key('left', 1.0)
                                else:
                                    self.input_controller.hold_key('right', 1.0)
                                
                                time.sleep(0.3)
                            else:
                                # Random turns to explore (looking for orange)
                                if random.random() < 0.03:  # 3% chance
                                    self.input_controller.release_key('w')
                                    if random.choice([True, False]):
                                        self.input_controller.hold_key('left', 0.5)
                                    else:
                                        self.input_controller.hold_key('right', 0.5)
                                    time.sleep(0.2)
                            
                            time.sleep(0.1)  # Slower when not tracking
                    else:
                        # Screenshot failed, keep walking
                        self.input_controller.press_key('w')
                        time.sleep(0.1)
                else:
                    # Bot is inactive, release all keys and wait
                    self.input_controller.release_all()
                    time.sleep(0.5)
                    continue
                
            except Exception as e:
                self.logger.error(f"Error in movement loop: {e}")
                self.input_controller.release_all()
                time.sleep(1)
    
    def start(self):
        """Start the bot system (not the bot behavior - use F1 for that)"""
        self.logger.info("Starting Cipher Bot system...")
        
        if not self.find_roblox_window():
            return False
        
        self.running = True
        # Don't auto-start the bot - wait for F1
        self.bot_active = False
        
        # Start the chat facts thread
        chat_thread = threading.Thread(target=self.chat_facts_loop, daemon=True)
        chat_thread.start()
        
        self.logger.info("🎮 Bot system ready!")
        self.logger.info("Press F1 to START the bot")
        self.logger.info("Press F2 to STOP the bot")
        self.logger.info("Press Ctrl+C to exit completely")
        
        # NO CHAT MESSAGES
        
        try:
            # Run the main movement loop
            self.movement_loop()
        except KeyboardInterrupt:
            self.logger.info("Bot system stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop the bot system"""
        self.logger.info("Stopping Cipher Bot system...")
        self.running = False
        self.bot_active = False
        
        # Release any held keys
        pyautogui.keyUp('w')
        pyautogui.keyUp('a')
        pyautogui.keyUp('s')
        pyautogui.keyUp('d')
        
        # Clean up hotkeys
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        
        self.logger.info("Bot system stopped successfully")

def main():
    print("="*50)
    print("       CIPHER V1 RBOT - ROBLOX AI BOT")
    print("="*50)
    print("Features:")
    print("• Intelligent pathfinding and wall avoidance")
    print("• Automatic fact sharing in chat")
    print("• Adaptive movement patterns")
    print("• Real-time obstacle detection")
    print("• F1/F2 hotkey controls")
    print("="*50)
    print()
    
    bot = CipherBot()
    
    print("Instructions:")
    print("1. Make sure Roblox is running and you're in a game")
    print("   📍 IMPORTANT: You must be IN A GAME, not just the Roblox launcher!")
    print("   📍 Join any game (like Adopt Me, Bloxburg, etc.)")
    print("2. Position your character in an open area")
    print("3. Press Enter to initialize the bot system")
    print("4. Use F1 to START the bot behavior")
    print("5. Use F2 to STOP the bot behavior")
    print("6. Press Ctrl+C to exit completely")
    print()
    print("🎮 The bot will wait for F1 after initialization!")
    print("🔧 If you get errors, run: python window_detector.py")
    print()
    
    input("Press Enter to initialize the bot system...")
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\nBot system stopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()