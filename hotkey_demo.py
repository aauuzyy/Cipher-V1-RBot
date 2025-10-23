"""
Hotkey Demo for Cipher V1 RBot
Shows how the F1/F2 controls work
"""

import time
import keyboard
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class HotkeyDemo:
    def __init__(self):
        self.running = True
        self.bot_active = False
        self.setup_hotkeys()
    
    def setup_hotkeys(self):
        """Setup F1 and F2 hotkeys"""
        keyboard.add_hotkey('f1', self.start_demo)
        keyboard.add_hotkey('f2', self.stop_demo)
        keyboard.add_hotkey('esc', self.exit_demo)
        logger.info("Demo hotkeys registered:")
        logger.info("  F1 = Start Bot Demo")
        logger.info("  F2 = Stop Bot Demo") 
        logger.info("  ESC = Exit Demo")
    
    def start_demo(self):
        """Start demo via F1"""
        if not self.bot_active:
            self.bot_active = True
            logger.info("🟢 BOT DEMO STARTED! (Bot would be walking and chatting now)")
    
    def stop_demo(self):
        """Stop demo via F2"""
        if self.bot_active:
            self.bot_active = False
            logger.info("🔴 BOT DEMO STOPPED! (Bot would be idle now)")
    
    def exit_demo(self):
        """Exit demo via ESC"""
        self.running = False
        logger.info("🚪 EXITING DEMO...")
    
    def run(self):
        """Run the demo"""
        print("="*60)
        print("     CIPHER V1 RBOT - HOTKEY DEMO")
        print("="*60)
        print()
        print("This demo shows how the F1/F2 hotkeys work!")
        print()
        print("Controls:")
        print("  F1  = Start the bot (simulates bot activation)")
        print("  F2  = Stop the bot (simulates bot deactivation)")
        print("  ESC = Exit this demo")
        print()
        print("The actual bot will walk around and chat when started.")
        print("This demo just shows the hotkey detection working.")
        print()
        print("Press F1 to test starting the bot...")
        print()
        
        try:
            while self.running:
                if self.bot_active:
                    print("🤖 Bot is ACTIVE - would be walking and chatting...", end='\r')
                else:
                    print("😴 Bot is IDLE - waiting for F1 to activate...    ", end='\r')
                time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info("Demo stopped by Ctrl+C")
        
        keyboard.unhook_all_hotkeys()
        print("\n\nDemo finished! The actual bot works the same way.")
        print("Run 'python cipher_bot.py' to use the real bot!")

if __name__ == "__main__":
    demo = HotkeyDemo()
    demo.run()