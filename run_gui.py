import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import os

from gui import MaradminGUI
from setup_gui import EnvironmentSetupGUI

def check_environment():
    """Check if the environment is properly configured"""
    missing = []
    
    # Check required files
    if not Path('contacts.csv').exists():
        missing.append("contacts.csv file")
    if not Path('MCC Codes.csv').exists():
        missing.append("MCC Codes.csv file")
    
    # Check required directories
    if not Path('logs').exists():
        Path('logs').mkdir(exist_ok=True)
    
    # Check if any Slack webhooks are configured (optional)
    has_webhooks = (os.getenv('MARADMIN_SLACK_WEBHOOK_URL') or 
                   os.getenv('DELTA_SLACK_WEBHOOK_URL') or 
                   os.getenv('MFCC_SLACK_WEBHOOK_URL'))
    
    return missing, has_webhooks

def main():
    missing, has_webhooks = check_environment()
    
    if missing:
        if messagebox.askyesno("Setup Required", 
                              f"Some required components are missing:\n- {chr(10).join(missing)}\n\n"
                              "Would you like to run the setup wizard?"):
            root = tk.Tk()
            app = EnvironmentSetupGUI(root)
            root.mainloop()
            return
        
    elif not has_webhooks:
        if messagebox.askyesno("Optional Setup", 
                              "No Slack webhooks are configured. While optional, they enable notifications.\n\n"
                              "Would you like to run the setup wizard to configure them?"):
            root = tk.Tk()
            app = EnvironmentSetupGUI(root)
            root.mainloop()
            return
    
    # Run main GUI
    root = tk.Tk()
    app = MaradminGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
