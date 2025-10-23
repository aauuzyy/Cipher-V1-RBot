"""
Simple GUI Test - Check if tkinter window opens
"""
import tkinter as tk
from tkinter import messagebox

def test_gui():
    """Test if GUI opens properly"""
    root = tk.Tk()
    root.title("Cipher GUI Test")
    root.geometry("400x300")
    root.configure(bg='#1a1a1a')
    
    # Add test content
    label = tk.Label(root, text="Cipher V1 RBot GUI Test", 
                    fg='white', bg='#1a1a1a', 
                    font=('Arial', 16, 'bold'))
    label.pack(pady=50)
    
    button = tk.Button(root, text="GUI Working!", 
                      command=lambda: messagebox.showinfo("Success", "GUI is working!"),
                      bg='#00bcd4', fg='white',
                      font=('Arial', 12))
    button.pack(pady=20)
    
    close_button = tk.Button(root, text="Close Test", 
                           command=root.destroy,
                           bg='#f44336', fg='white',
                           font=('Arial', 12))
    close_button.pack(pady=10)
    
    # Make sure window appears on top
    root.lift()
    root.attributes('-topmost', True)
    root.after(1000, lambda: root.attributes('-topmost', False))
    
    root.mainloop()

if __name__ == "__main__":
    test_gui()