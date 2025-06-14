#!/usr/bin/env python3
"""
MARADMIN Alert System - First Time Setup
Run this script to set up your environment for the first time.
"""

import tkinter as tk
from setup_gui import EnvironmentSetupGUI

def main():
    print("Starting MARADMIN Alert System Setup...")
    print("This will help you configure your environment for the first time.")
    print("Opening setup GUI...")
    
    root = tk.Tk()
    app = EnvironmentSetupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
