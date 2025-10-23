"""
Cipher GUI Launcher with startup message
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def launch_gui():
    """Launch the main GUI"""
    try:
        # Show startup message
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        messagebox.showinfo("Cipher V1 RBot", 
                           "Starting Cipher V1 RBot Professional Interface...\n\n" +
                           "The main window will open shortly!")
        
        root.destroy()
        
        # Launch the main GUI
        script_dir = os.path.dirname(os.path.abspath(__file__))
        python_exe = os.path.join(script_dir, '.venv', 'Scripts', 'python.exe')
        gui_script = os.path.join(script_dir, 'cipher_gui.py')
        
        if os.path.exists(python_exe) and os.path.exists(gui_script):
            subprocess.run([python_exe, gui_script])
        else:
            messagebox.showerror("Error", "Python environment or GUI script not found!")
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch GUI: {str(e)}")

if __name__ == "__main__":
    launch_gui()