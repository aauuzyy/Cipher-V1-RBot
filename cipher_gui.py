"""
Cipher V1 RBot - Professional GUI with Orca Hub Aesthetic
Advanced interface with frost effects, purple glows, and smooth animations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import subprocess
import json
import math

# Add the bot module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from cipher_bot import CipherBot
except ImportError:
    CipherBot = None

class ModernButton(tk.Canvas):
    """Custom button with glow effects and animations"""
    def __init__(self, parent, text, command=None, bg_color="#8B5CF6", hover_color="#A855F7", 
                 text_color="white", width=200, height=50, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, 
                        bg=parent['bg'], **kwargs)
        
        self.command = command
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height
        self.is_hovered = False
        self.glow_intensity = 0
        
        self.draw_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self):
        """Draw the button with smooth glow effect"""
        self.delete("all")
        
        # Create smooth glow effect with multiple layers
        if self.glow_intensity > 0:
            # Multiple glow layers for smooth effect
            for i in range(8, 0, -1):
                alpha = int(20 * self.glow_intensity * (8 - i) / 8)
                glow_radius = i * 3
                self.create_oval(self.width//2 - glow_radius, self.height//2 - glow_radius,
                               self.width//2 + glow_radius, self.height//2 + glow_radius,
                               outline=f"#{hex(139)[2:].zfill(2)}{hex(92)[2:].zfill(2)}{hex(246)[2:].zfill(2)}", 
                               width=2, fill="")
        
        # Main button background with smooth edges
        color = self.hover_color if self.is_hovered else self.bg_color
        self.create_rounded_rect(8, 8, self.width-8, self.height-8, radius=12, 
                               fill=color, outline="#A855F7", width=1)
        
        # Button text
        self.create_text(self.width//2, self.height//2, text=self.text, 
                        fill=self.text_color, font=("Segoe UI", 11, "bold"))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
        """Create a rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        if self.command:
            self.command()
    
    def on_enter(self, event):
        self.is_hovered = True
        self.animate_glow(True)
    
    def on_leave(self, event):
        self.is_hovered = False
        self.animate_glow(False)
    
    def animate_glow(self, increase):
        """Animate the glow effect"""
        target = 1.0 if increase else 0.0
        step = 0.1 if increase else -0.1
        
        def animate():
            if (increase and self.glow_intensity < target) or (not increase and self.glow_intensity > target):
                self.glow_intensity += step
                self.glow_intensity = max(0, min(1, self.glow_intensity))
                self.draw_button()
                self.after(20, animate)
        
        animate()

class FrostFrame(tk.Frame):
    """Custom frame with dark gray frosted effect"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#2d2d2d")

class CipherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.bot = None
        self.bot_thread = None
        self.is_running = False
        self.is_active = False
        
        # Animation variables
        self.pulse_phase = 0
        self.status_lights = {}
        
        # Load configuration
        self.load_config()
        
        # Setup the main window
        self.setup_window()
        
        # Create the interface
        self.create_interface()
        
        # Start animations
        self.start_animations()
        
        # Start status updates
        self.update_status()
    
    def load_config(self):
        """Load bot configuration"""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "movement": {"fact_interval": 30, "wall_detection_threshold": 50},
                "chat": {"enable_facts": True}
            }
    
    def setup_window(self):
        """Setup the main window with smooth dark gray aesthetic"""
        self.root.title("Cipher V1 RBot")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a1a')  # Dark gray background
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make window appear on top initially
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(1000, lambda: self.root.attributes('-topmost', False))
        
        # Configure styles
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles with dark gray theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark gray theme colors
        bg_primary = '#1a1a1a'      # Main dark gray
        bg_secondary = '#2d2d2d'    # Lighter gray panels
        bg_tertiary = '#3d3d3d'     # Even lighter gray
        accent_purple = '#8B5CF6'   # Purple accent
        accent_cyan = '#06B6D4'     # Cyan accent
        text_primary = '#FFFFFF'    # White text
        text_secondary = '#B4B4B8'  # Light gray text
    
    def create_frosted_background(self, width, height):
        """Create smooth dark gray background with subtle patterns"""
        # Create base dark gray image
        img = Image.new('RGB', (width, height), '#1a1a1a')
        draw = ImageDraw.Draw(img)
        
        # Add very subtle geometric pattern
        pattern_color = '#2a2a2a'
        
        # Create diagonal grid pattern
        for x in range(0, width, 60):
            for y in range(0, height, 60):
                # Draw subtle squares
                draw.rectangle([x, y, x+30, y+30], fill=pattern_color)
        
        # Add subtle diagonal lines
        for i in range(0, width + height, 80):
            draw.line([(i, 0), (i - height, height)], fill='#222222', width=1)
            draw.line([(i - 20, 0), (i - height - 20, height)], fill='#1e1e1e', width=1)
        
        # Apply very light blur for smoothness
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        return ImageTk.PhotoImage(img)
    
    def create_rounded_rect_simple(self, canvas, x1, y1, x2, y2, fill_color, outline_color):
        """Create a simple rounded rectangle"""
        radius = 10
        canvas.create_oval(x1, y1, x1 + radius, y1 + radius, fill=fill_color, outline=outline_color, width=2)
        canvas.create_oval(x2 - radius, y1, x2, y1 + radius, fill=fill_color, outline=outline_color, width=2)
        canvas.create_oval(x1, y2 - radius, x1 + radius, y2, fill=fill_color, outline=outline_color, width=2)
        canvas.create_oval(x2 - radius, y2 - radius, x2, y2, fill=fill_color, outline=outline_color, width=2)
        canvas.create_rectangle(x1 + radius//2, y1, x2 - radius//2, y2, fill=fill_color, outline="")
        canvas.create_rectangle(x1, y1 + radius//2, x2, y2 - radius//2, fill=fill_color, outline="")
    
    def create_logo(self):
        """Create the C4 logo with smooth glow effect"""
        size = 100
        img = Image.new('RGBA', (size + 40, size + 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create smooth glow effect using multiple layers
        center_x, center_y = (size + 40) // 2, (size + 40) // 2
        
        # Outer glow - multiple soft layers
        for radius in range(25, 5, -2):
            alpha = int(15 * (25 - radius) / 20)
            glow_color = (139, 92, 246, alpha)
            draw.ellipse([center_x - radius, center_y - radius, 
                         center_x + radius, center_y + radius], 
                        fill=glow_color)
        
        # Main circle with gradient effect
        main_radius = 45
        draw.ellipse([center_x - main_radius, center_y - main_radius, 
                     center_x + main_radius, center_y + main_radius], 
                    fill=(139, 92, 246, 255), outline=(168, 85, 247, 255), width=2)
        
        # Inner highlight circle for depth
        inner_radius = 35
        draw.ellipse([center_x - inner_radius, center_y - inner_radius, 
                     center_x + inner_radius, center_y + inner_radius], 
                    fill=(160, 120, 250, 80))
        
        # Apply blur for smooth glow
        img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
        
        # Re-draw the main elements on top for sharpness
        draw = ImageDraw.Draw(img)
        draw.ellipse([center_x - main_radius, center_y - main_radius, 
                     center_x + main_radius, center_y + main_radius], 
                    fill=(139, 92, 246, 255), outline=(168, 85, 247, 255), width=2)
        
        # C4 text with smooth anti-aliasing
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = None
        
        # Text with subtle glow
        for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((center_x + offset[0], center_y + offset[1]), 
                     'C4', fill=(255, 255, 255, 150), font=font, anchor='mm')
        
        # Main text
        draw.text((center_x, center_y), 'C4', fill='white', font=font, anchor='mm')
        
        return ImageTk.PhotoImage(img)
    
    def create_interface(self):
        """Create the main interface with Orca Hub styling"""
        # Main background
        bg_image = self.create_frosted_background(900, 700)
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0)
        
        # Add subtle border glow behind the container
        border_canvas = tk.Canvas(self.root, highlightthickness=0, bg="#1a1a1a")
        border_canvas.place(x=45, y=45, width=810, height=610)
        border_canvas.create_rectangle(5, 5, 805, 605, outline="#8B5CF6", width=2)
        
        # Create main container with dark gray frosted effect
        main_container = FrostFrame(self.root, bg="#2d2d2d")
        main_container.place(x=50, y=50, width=800, height=600)
        
        # Header section
        self.create_header(main_container)
        
        # Profile section (like Orca Hub)
        self.create_profile_section(main_container)
        
        # Control panels
        self.create_control_sections(main_container)
        
        # Status indicators
        self.create_status_section(main_container)
    
    def create_header(self, parent):
        """Create header with logo and title"""
        header_frame = FrostFrame(parent, bg="#3d3d3d", height=80)
        header_frame.place(x=20, y=20, width=760, height=80)
        
        # Logo
        logo = self.create_logo()
        logo_label = tk.Label(header_frame, image=logo, bg="#3d3d3d")
        logo_label.image = logo
        logo_label.place(x=20, y=-10)
        
        # Title with smooth glow effect
        title_canvas = tk.Canvas(header_frame, width=400, height=80, 
                               highlightthickness=0, bg="#3d3d3d")
        title_canvas.place(x=140, y=0)
        
        # Title with subtle glow
        title_canvas.create_text(202, 25, text="Cipher V1 RBot", 
                               fill="#8B5CF6", font=("Segoe UI", 20, "bold"))
        title_canvas.create_text(200, 23, text="Cipher V1 RBot", 
                               fill="white", font=("Segoe UI", 20, "bold"))
        
        # Subtitle
        title_canvas.create_text(200, 45, text="Advanced AI Automation", 
                               fill="#B4B4B8", font=("Segoe UI", 12))
        
        # Version badge
        version_canvas = tk.Canvas(header_frame, width=100, height=30, 
                                 highlightthickness=0, bg="#3d3d3d")
        version_canvas.place(x=640, y=25)
        self.create_rounded_rect_simple(version_canvas, 0, 0, 100, 30, "#8B5CF6", "#A855F7")
        version_canvas.create_text(50, 15, text="v1.0 PRO", fill="white", 
                                 font=("Segoe UI", 9, "bold"))
    
    def create_profile_section(self, parent):
        """Create profile section with dark gray theme"""
        profile_frame = FrostFrame(parent, bg="#3d3d3d")
        profile_frame.place(x=20, y=120, width=250, height=200)
        
        # Profile circle
        profile_canvas = tk.Canvas(profile_frame, width=120, height=120, 
                                 highlightthickness=0, bg="#3d3d3d")
        profile_canvas.place(x=65, y=20)
        
        # Create animated profile ring
        self.profile_canvas = profile_canvas
        self.draw_profile_ring()
        
        # User info
        user_label = tk.Label(profile_frame, text="mirkoverov22", 
                            fg="white", bg="#3d3d3d", 
                            font=("Segoe UI", 14, "bold"))
        user_label.place(x=125, y=150, anchor="center")
        
        # Status badges
        stats_frame = FrostFrame(parent, bg="#3d3d3d")
        stats_frame.place(x=290, y=120, width=200, height=200)
        
        self.create_stats_badges(stats_frame)
    
    def draw_profile_ring(self):
        """Draw animated profile ring"""
        self.profile_canvas.delete("all")
        
        # Outer glow ring
        for i in range(3):
            alpha = int(100 - i * 30)
            self.profile_canvas.create_oval(10-i*2, 10-i*2, 110+i*2, 110+i*2, 
                                          outline="#8B5CF6", width=2)
        
        # Main profile circle with dark gray theme
        self.profile_canvas.create_oval(15, 15, 105, 105, 
                                      fill="#4d4d4d", outline="#8B5CF6", width=3)
        
        # Animated progress ring
        extent = int(270 + 90 * math.sin(self.pulse_phase))
        self.profile_canvas.create_arc(10, 10, 110, 110, start=0, extent=extent,
                                     outline="#06B6D4", width=4, style="arc")
        
        # Inner avatar placeholder
        self.profile_canvas.create_oval(25, 25, 95, 95, 
                                      fill="#8B5CF6", outline="white", width=2)
        self.profile_canvas.create_text(60, 60, text="C4", fill="white", 
                                      font=("Segoe UI", 16, "bold"))
    
    def create_stats_badges(self, parent):
        """Create stats badges like Orca Hub"""
        badges = [
            {"text": "Bot Active", "value": "Ready", "color": "#4ADE80"},
            {"text": "Uptime", "value": "0:00", "color": "#06B6D4"},
            {"text": "Status", "value": "Idle", "color": "#F59E0B"}
        ]
        
        for i, badge in enumerate(badges):
            badge_canvas = tk.Canvas(parent, width=180, height=50, 
                                   highlightthickness=0, bg="#3d3d3d")
            badge_canvas.place(x=10, y=20 + i * 60)
            
            # Badge background with dark gray theme
            self.create_rounded_rect_simple(badge_canvas, 5, 5, 175, 45, "#4d4d4d", badge["color"])
            
            # Badge text
            badge_canvas.create_text(20, 15, text=badge["text"], 
                                   fill="#B4B4B8", font=("Segoe UI", 9), anchor="w")
            badge_canvas.create_text(20, 30, text=badge["value"], 
                                   fill=badge["color"], font=("Segoe UI", 11, "bold"), anchor="w")
            
            # Store reference for updates
            setattr(self, f"badge_{i}_canvas", badge_canvas)
    
    def create_control_sections(self, parent):
        """Create control sections"""
        # Bot controls
        control_frame = FrostFrame(parent, bg="#2D2A3F")
        control_frame.place(x=510, y=120, width=270, height=320)
        
        # Control title
        title_label = tk.Label(control_frame, text="Bot Controls", 
                             fg="#8B5CF6", bg="#2D2A3F", 
                             font=("Segoe UI", 14, "bold"))
        title_label.place(x=20, y=20)
        
        # Control buttons with custom styling
        self.init_button = ModernButton(control_frame, "Initialize System", 
                                       command=self.start_bot_system,
                                       bg_color="#8B5CF6", width=230, height=45)
        self.init_button.place(x=20, y=60)
        
        self.activate_button = ModernButton(control_frame, "Activate Bot (F1)", 
                                          command=self.activate_bot,
                                          bg_color="#4ADE80", width=230, height=45)
        self.activate_button.place(x=20, y=120)
        
        self.deactivate_button = ModernButton(control_frame, "Deactivate Bot (F2)", 
                                            command=self.deactivate_bot,
                                            bg_color="#EF4444", width=230, height=45)
        self.deactivate_button.place(x=20, y=180)
        
        # Settings section
        settings_frame = FrostFrame(control_frame, bg="#3B3B4F")
        settings_frame.place(x=20, y=240, width=230, height=60)
        
        settings_label = tk.Label(settings_frame, text="Quick Settings", 
                                fg="#B4B4B8", bg="#3B3B4F", 
                                font=("Segoe UI", 10, "bold"))
        settings_label.place(x=10, y=10)
        
        # Facts toggle
        self.facts_var = tk.BooleanVar(value=True)
        facts_check = tk.Checkbutton(settings_frame, text="Enable Facts", 
                                   variable=self.facts_var,
                                   bg="#3B3B4F", fg="#B4B4B8", 
                                   selectcolor="#8B5CF6",
                                   font=("Segoe UI", 9))
        facts_check.place(x=10, y=30)
    
    def create_status_section(self, parent):
        """Create status indicators section"""
        status_frame = FrostFrame(parent, bg="#2D2A3F")
        status_frame.place(x=20, y=340, width=470, height=240)
        
        # Status title
        title_label = tk.Label(status_frame, text="System Status", 
                             fg="#8B5CF6", bg="#2D2A3F", 
                             font=("Segoe UI", 14, "bold"))
        title_label.place(x=20, y=20)
        
        # Status indicators with animated lights
        statuses = [
            {"text": "Roblox Connection", "key": "connection"},
            {"text": "Bot System", "key": "system"},
            {"text": "Bot Activity", "key": "activity"},
            {"text": "Window Detection", "key": "window"}
        ]
        
        for i, status in enumerate(statuses):
            y_pos = 60 + i * 40
            
            # Status light
            light_canvas = tk.Canvas(status_frame, width=20, height=20, 
                                   highlightthickness=0, bg="#2D2A3F")
            light_canvas.place(x=30, y=y_pos)
            
            # Status text
            status_label = tk.Label(status_frame, text=status["text"], 
                                  fg="#B4B4B8", bg="#2D2A3F", 
                                  font=("Segoe UI", 11))
            status_label.place(x=60, y=y_pos + 2)
            
            # Store references for animation
            self.status_lights[status["key"]] = {
                "canvas": light_canvas,
                "status": "disconnected",
                "pulse": 0
            }
        
        # Log area with modern styling
        log_label = tk.Label(status_frame, text="Activity Log", 
                           fg="#B4B4B8", bg="#2D2A3F", 
                           font=("Segoe UI", 10, "bold"))
        log_label.place(x=250, y=60)
        
        # Custom log area with frosted background
        log_bg = FrostFrame(status_frame, bg="#1F1B2E")
        log_bg.place(x=250, y=85, width=200, height=130)
        
        self.log_text = tk.Text(log_bg, bg="#1F1B2E", fg="#B4B4B8", 
                              font=("Consolas", 8), relief="flat", 
                              borderwidth=0, insertbackground="#8B5CF6")
        self.log_text.place(x=5, y=5, width=190, height=120)
    
    def start_animations(self):
        """Start all animations"""
        self.animate_pulse()
        self.animate_status_lights()
    
    def animate_pulse(self):
        """Animate pulsing effects"""
        self.pulse_phase += 0.1
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase = 0
        
        # Update profile ring
        if hasattr(self, 'profile_canvas'):
            self.draw_profile_ring()
        
        # Schedule next frame
        self.root.after(50, self.animate_pulse)
    
    def animate_status_lights(self):
        """Animate status indicator lights"""
        for key, light_data in self.status_lights.items():
            canvas = light_data["canvas"]
            status = light_data["status"]
            light_data["pulse"] += 0.2
            
            canvas.delete("all")
            
            # Color based on status
            if status == "connected":
                color = "#4ADE80"
                glow_color = "#22C55E"
            elif status == "active":
                color = "#06B6D4"
                glow_color = "#0891B2"
            elif status == "warning":
                color = "#F59E0B"
                glow_color = "#D97706"
            else:  # disconnected
                color = "#EF4444"
                glow_color = "#DC2626"
            
            # Pulsing glow effect
            pulse_intensity = (math.sin(light_data["pulse"]) + 1) / 2
            
            # Outer glow
            for i in range(3):
                alpha_factor = (3 - i) / 3 * pulse_intensity
                canvas.create_oval(2-i, 2-i, 18+i, 18+i, 
                                 outline=glow_color, width=1)
            
            # Main light
            canvas.create_oval(4, 4, 16, 16, fill=color, outline=glow_color, width=2)
            
            # Inner highlight
            canvas.create_oval(6, 6, 10, 10, fill="white", outline="")
        
        # Schedule next frame
        self.root.after(100, self.animate_status_lights)
    
    def log_message(self, message):
        """Add message to log with styling"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Keep only last 50 lines
        lines = self.log_text.get("1.0", tk.END).split('\n')
        if len(lines) > 50:
            self.log_text.delete("1.0", f"{len(lines)-50}.0")
    
    def start_bot_system(self):
        """Initialize the bot system"""
        if self.is_running:
            messagebox.showwarning("Warning", "Bot system is already running!")
            return
        
        if CipherBot is None:
            messagebox.showerror("Error", "Bot module not found!")
            return
        
        try:
            self.bot = CipherBot()
            self.bot_thread = threading.Thread(target=self.run_bot_system, daemon=True)
            self.bot_thread.start()
            
            self.is_running = True
            self.log_message("Bot system initialized successfully")
            
            # Update status lights
            self.status_lights["system"]["status"] = "connected"
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")
            self.log_message(f"Error: {str(e)}")
    
    def run_bot_system(self):
        """Run the bot system in background thread"""
        try:
            self.bot.start()
        except Exception as e:
            self.log_message(f"Bot error: {str(e)}")
    
    def activate_bot(self):
        """Activate the bot"""
        if self.bot and hasattr(self.bot, 'start_bot_hotkey'):
            self.bot.start_bot_hotkey()
            self.is_active = True
            self.status_lights["activity"]["status"] = "active"
            self.log_message("Bot activated - Now walking and chatting")
    
    def deactivate_bot(self):
        """Deactivate the bot"""
        if self.bot and hasattr(self.bot, 'stop_bot_hotkey'):
            self.bot.stop_bot_hotkey()
            self.is_active = False
            self.status_lights["activity"]["status"] = "warning"
            self.log_message("Bot deactivated - Now idle")
    
    def update_status(self):
        """Update status indicators"""
        if self.bot:
            # Update connection status
            if hasattr(self.bot, 'roblox_window') and self.bot.roblox_window:
                self.status_lights["connection"]["status"] = "connected"
                self.status_lights["window"]["status"] = "connected"
            else:
                self.status_lights["connection"]["status"] = "disconnected"
                self.status_lights["window"]["status"] = "disconnected"
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

# Add rounded rectangle method to Canvas
def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
    """Create a rounded rectangle on canvas"""
    points = []
    for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                 (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                 (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                 (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
        points.extend([x, y])
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_rounded_rect = create_rounded_rect

def main():
    """Main entry point"""
    app = CipherGUI()
    app.run()

if __name__ == "__main__":
    main()
    
    def setup_window(self):
        """Setup the main window with professional styling"""
        self.root.title("Cipher V1 RBot - Professional Interface")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a1a')
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make sure window appears on top initially
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(1000, lambda: self.root.attributes('-topmost', False))
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Configure ttk styles
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles for a professional look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom colors
        bg_dark = '#1a1a1a'
        bg_medium = '#2d2d2d'
        bg_light = '#3d3d3d'
        accent = '#00bcd4'
        text_color = '#ffffff'
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=bg_dark, 
                       foreground=text_color, 
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Status.TLabel',
                       background=bg_medium,
                       foreground=text_color,
                       font=('Segoe UI', 10))
        
        style.configure('Info.TLabel',
                       background=bg_dark,
                       foreground='#cccccc',
                       font=('Segoe UI', 9))
        
        style.configure('Professional.TButton',
                       background=accent,
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Professional.TButton',
                  background=[('active', '#00acc1'),
                             ('pressed', '#0097a7')])
    
    def create_textured_background(self, width, height):
        """Create a textured background similar to Orca Hub"""
        # Create base image
        img = Image.new('RGB', (width, height), '#1a1a1a')
        draw = ImageDraw.Draw(img)
        
        # Add subtle texture lines
        line_color = '#252525'
        
        # Vertical lines
        for x in range(0, width, 20):
            draw.line([(x, 0), (x, height)], fill=line_color, width=1)
        
        # Horizontal lines
        for y in range(0, height, 20):
            draw.line([(0, y), (width, y)], fill=line_color, width=1)
        
        # Add diagonal pattern
        for x in range(0, width + height, 40):
            draw.line([(x, 0), (x - height, height)], fill='#222222', width=1)
        
        return ImageTk.PhotoImage(img)
    
    def create_logo_placeholder(self):
        """Create a C4 logo placeholder"""
        size = 80
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create circular background
        draw.ellipse([5, 5, size-5, size-5], fill='#00bcd4', outline='#ffffff', width=3)
        
        # Add C4 text
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = None
        
        draw.text((size//2, size//2), 'C4', fill='white', font=font, anchor='mm')
        
        return ImageTk.PhotoImage(img)
    
    def create_interface(self):
        """Create the main interface"""
        # Create textured background
        bg_image = self.create_textured_background(800, 600)
        bg_label = tk.Label(self.root, image=bg_image, bg='#1a1a1a')
        bg_label.image = bg_image  # Keep reference
        bg_label.place(x=0, y=0)
        
        # Header section
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create the header with logo and title"""
        header_frame = tk.Frame(self.root, bg='#2d2d2d', height=100)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Logo
        logo = self.create_logo_placeholder()
        logo_label = tk.Label(header_frame, image=logo, bg='#2d2d2d')
        logo_label.image = logo
        logo_label.pack(side='left', padx=20, pady=10)
        
        # Title and info
        title_frame = tk.Frame(header_frame, bg='#2d2d2d')
        title_frame.pack(side='left', fill='both', expand=True, padx=20)
        
        title_label = ttk.Label(title_frame, text="Cipher V1 RBot", style='Title.TLabel')
        title_label.pack(anchor='w', pady=(15, 5))
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Advanced AI-Powered Roblox Automation", 
                                  style='Info.TLabel')
        subtitle_label.pack(anchor='w')
        
        version_label = ttk.Label(title_frame, 
                                 text="Version 1.0 • Professional Edition", 
                                 style='Info.TLabel')
        version_label.pack(anchor='w', pady=(5, 0))
    
    def create_main_content(self):
        """Create the main content area"""
        content_frame = tk.Frame(self.root, bg='#1a1a1a')
        content_frame.pack(fill='both', expand=True, padx=20)
        
        # Left panel - Bot Status
        left_panel = tk.Frame(content_frame, bg='#2d2d2d', width=350)
        left_panel.pack(side='left', fill='y', padx=(0, 10), pady=10)
        left_panel.pack_propagate(False)
        
        self.create_bot_status_panel(left_panel)
        
        # Right panel - Configuration
        right_panel = tk.Frame(content_frame, bg='#2d2d2d')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=10)
        
        self.create_config_panel(right_panel)
    
    def create_bot_status_panel(self, parent):
        """Create bot status and control panel"""
        # Title
        title_label = ttk.Label(parent, text="Bot Status", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Status indicators
        self.status_frame = tk.Frame(parent, bg='#2d2d2d')
        self.status_frame.pack(fill='x', padx=20, pady=10)
        
        # Connection status
        self.connection_status = tk.Label(self.status_frame, 
                                         text="● Disconnected", 
                                         fg='#ff5555', bg='#2d2d2d',
                                         font=('Segoe UI', 10, 'bold'))
        self.connection_status.pack(anchor='w', pady=5)
        
        # Bot status
        self.bot_status = tk.Label(self.status_frame, 
                                  text="● Inactive", 
                                  fg='#ffaa00', bg='#2d2d2d',
                                  font=('Segoe UI', 10, 'bold'))
        self.bot_status.pack(anchor='w', pady=5)
        
        # Window status
        self.window_status = tk.Label(self.status_frame, 
                                     text="● No Roblox Window", 
                                     fg='#ff5555', bg='#2d2d2d',
                                     font=('Segoe UI', 10, 'bold'))
        self.window_status.pack(anchor='w', pady=5)
        
        # Control buttons
        button_frame = tk.Frame(parent, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.start_button = tk.Button(button_frame, 
                                     text="Initialize Bot System",
                                     bg='#00bcd4', fg='white',
                                     font=('Segoe UI', 12, 'bold'),
                                     relief='flat', borderwidth=0,
                                     command=self.start_bot_system)
        self.start_button.pack(fill='x', pady=5)
        
        self.activate_button = tk.Button(button_frame, 
                                        text="Activate Bot (F1)",
                                        bg='#4caf50', fg='white',
                                        font=('Segoe UI', 12, 'bold'),
                                        relief='flat', borderwidth=0,
                                        state='disabled',
                                        command=self.activate_bot)
        self.activate_button.pack(fill='x', pady=5)
        
        self.deactivate_button = tk.Button(button_frame, 
                                          text="Deactivate Bot (F2)",
                                          bg='#f44336', fg='white',
                                          font=('Segoe UI', 12, 'bold'),
                                          relief='flat', borderwidth=0,
                                          state='disabled',
                                          command=self.deactivate_bot)
        self.deactivate_button.pack(fill='x', pady=5)
        
        # Log area
        log_label = ttk.Label(parent, text="Activity Log", style='Info.TLabel')
        log_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        log_frame = tk.Frame(parent, bg='#2d2d2d')
        log_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.log_text = tk.Text(log_frame, 
                               bg='#1a1a1a', fg='#cccccc',
                               font=('Consolas', 9),
                               relief='flat', borderwidth=0,
                               height=8)
        
        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_config_panel(self, parent):
        """Create configuration panel"""
        # Title
        title_label = ttk.Label(parent, text="Configuration", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Configuration options
        config_frame = tk.Frame(parent, bg='#2d2d2d')
        config_frame.pack(fill='both', expand=True, padx=20)
        
        # Movement settings
        movement_label = tk.Label(config_frame, text="Movement Settings", 
                                 fg='#00bcd4', bg='#2d2d2d',
                                 font=('Segoe UI', 11, 'bold'))
        movement_label.pack(anchor='w', pady=(0, 10))
        
        # Wall detection threshold
        threshold_frame = tk.Frame(config_frame, bg='#2d2d2d')
        threshold_frame.pack(fill='x', pady=5)
        
        tk.Label(threshold_frame, text="Wall Detection Sensitivity:", 
                fg='#cccccc', bg='#2d2d2d', font=('Segoe UI', 9)).pack(anchor='w')
        
        self.threshold_var = tk.IntVar(value=self.config.get('movement', {}).get('wall_detection_threshold', 50))
        threshold_scale = tk.Scale(threshold_frame, from_=10, to=100, 
                                  orient='horizontal', variable=self.threshold_var,
                                  bg='#2d2d2d', fg='#cccccc', 
                                  highlightthickness=0, relief='flat')
        threshold_scale.pack(fill='x', pady=(5, 15))
        
        # Chat settings
        chat_label = tk.Label(config_frame, text="Chat Settings", 
                             fg='#00bcd4', bg='#2d2d2d',
                             font=('Segoe UI', 11, 'bold'))
        chat_label.pack(anchor='w', pady=(10, 10))
        
        # Fact interval
        interval_frame = tk.Frame(config_frame, bg='#2d2d2d')
        interval_frame.pack(fill='x', pady=5)
        
        tk.Label(interval_frame, text="Fact Sharing Interval (seconds):", 
                fg='#cccccc', bg='#2d2d2d', font=('Segoe UI', 9)).pack(anchor='w')
        
        self.interval_var = tk.IntVar(value=self.config.get('chat', {}).get('fact_interval', 30))
        interval_scale = tk.Scale(interval_frame, from_=10, to=120, 
                                 orient='horizontal', variable=self.interval_var,
                                 bg='#2d2d2d', fg='#cccccc', 
                                 highlightthickness=0, relief='flat')
        interval_scale.pack(fill='x', pady=(5, 15))
        
        # Enable facts checkbox
        self.facts_var = tk.BooleanVar(value=self.config.get('chat', {}).get('enable_facts', True))
        facts_check = tk.Checkbutton(config_frame, text="Enable Fact Sharing",
                                    variable=self.facts_var,
                                    bg='#2d2d2d', fg='#cccccc',
                                    selectcolor='#1a1a1a',
                                    font=('Segoe UI', 9))
        facts_check.pack(anchor='w', pady=5)
        
        # Save config button
        save_button = tk.Button(config_frame, 
                               text="Save Configuration",
                               bg='#ff9800', fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               relief='flat', borderwidth=0,
                               command=self.save_config)
        save_button.pack(fill='x', pady=(20, 0))
        
        # Instructions
        instructions_label = tk.Label(config_frame, text="Instructions", 
                                     fg='#00bcd4', bg='#2d2d2d',
                                     font=('Segoe UI', 11, 'bold'))
        instructions_label.pack(anchor='w', pady=(30, 10))
        
        instructions = """1. Join a Roblox game first
2. Click 'Initialize Bot System'
3. Use 'Activate Bot' or press F1
4. Use 'Deactivate Bot' or press F2
5. Bot will walk and share facts automatically"""
        
        instructions_text = tk.Label(config_frame, text=instructions,
                                   fg='#cccccc', bg='#2d2d2d',
                                   font=('Segoe UI', 9),
                                   justify='left')
        instructions_text.pack(anchor='w')
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_bar = tk.Frame(self.root, bg='#333333', height=30)
        status_bar.pack(fill='x', side='bottom')
        status_bar.pack_propagate(False)
        
        self.status_text = tk.Label(status_bar, 
                                   text="Ready - Join a Roblox game to begin",
                                   bg='#333333', fg='#cccccc',
                                   font=('Segoe UI', 9))
        self.status_text.pack(side='left', padx=10, pady=5)
        
        # Version info
        version_text = tk.Label(status_bar, 
                               text="Cipher V1 RBot v1.0",
                               bg='#333333', fg='#666666',
                               font=('Segoe UI', 8))
        version_text.pack(side='right', padx=10, pady=5)
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Keep only last 100 lines
        lines = self.log_text.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete("1.0", f"{len(lines)-100}.0")
    
    def start_bot_system(self):
        """Initialize the bot system"""
        if self.is_running:
            messagebox.showwarning("Warning", "Bot system is already running!")
            return
        
        if CipherBot is None:
            messagebox.showerror("Error", "Bot module not found!")
            return
        
        try:
            self.bot = CipherBot()
            self.bot_thread = threading.Thread(target=self.run_bot_system, daemon=True)
            self.bot_thread.start()
            
            self.start_button.config(state='disabled', text="System Running")
            self.activate_button.config(state='normal')
            self.deactivate_button.config(state='normal')
            
            self.is_running = True
            self.log_message("Bot system initialized successfully")
            self.status_text.config(text="Bot system running - Use F1/F2 or buttons to control")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")
            self.log_message(f"Error: {str(e)}")
    
    def run_bot_system(self):
        """Run the bot system in background thread"""
        try:
            self.bot.start()
        except Exception as e:
            self.log_message(f"Bot error: {str(e)}")
    
    def activate_bot(self):
        """Activate the bot"""
        if self.bot and hasattr(self.bot, 'start_bot_hotkey'):
            self.bot.start_bot_hotkey()
            self.is_active = True
            self.log_message("Bot activated - Now walking and chatting")
    
    def deactivate_bot(self):
        """Deactivate the bot"""
        if self.bot and hasattr(self.bot, 'stop_bot_hotkey'):
            self.bot.stop_bot_hotkey()
            self.is_active = False
            self.log_message("Bot deactivated - Now idle")
    
    def save_config(self):
        """Save configuration to file"""
        config = {
            "movement": {
                "wall_detection_threshold": self.threshold_var.get()
            },
            "chat": {
                "fact_interval": self.interval_var.get(),
                "enable_facts": self.facts_var.get()
            }
        }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            self.log_message("Configuration saved successfully")
            messagebox.showinfo("Success", "Configuration saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
    
    def update_status(self):
        """Update status indicators"""
        if self.bot:
            # Update connection status
            if hasattr(self.bot, 'roblox_window') and self.bot.roblox_window:
                self.connection_status.config(text="● Connected", fg='#4caf50')
                self.window_status.config(text="● Roblox Window Found", fg='#4caf50')
            else:
                self.connection_status.config(text="● Disconnected", fg='#ff5555')
                self.window_status.config(text="● No Roblox Window", fg='#ff5555')
            
            # Update bot status
            if hasattr(self.bot, 'bot_active') and self.bot.bot_active:
                self.bot_status.config(text="● Active", fg='#4caf50')
            else:
                self.bot_status.config(text="● Inactive", fg='#ffaa00')
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = CipherGUI()
    app.run()

if __name__ == "__main__":
    main()