import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import csv
from pathlib import Path
import requests
import zipfile
import shutil
import platform

class EnvironmentSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MARADMIN Alert - Environment Setup")
        self.root.geometry("900x700")
        
        # Create main frame with scrollbar
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Main content frame
        main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="MARADMIN Alert System - First Time Setup", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Progress tracking
        self.setup_steps = {
            "python_packages": False,
            "chrome_driver": False,
            "env_variables": False,
            "csv_files": False
        }
        
        self.create_sections(main_frame)
        
        # Final setup button
        self.final_button = ttk.Button(main_frame, text="Complete Setup & Test", 
                                     command=self.complete_setup, state="disabled")
        self.final_button.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Complete all sections above to finish setup")
        self.status_label.pack()
        
        # Check initial status
        self.check_all_status()

    def create_sections(self, parent):
        # Section 1: Python Packages
        self.create_package_section(parent)
        
        # Section 2: Chrome/ChromeDriver
        self.create_chrome_section(parent)
        
        # Section 3: Environment Variables
        self.create_env_section(parent)
        
        # Section 4: CSV Files
        self.create_csv_section(parent)

    def create_package_section(self, parent):
        frame = ttk.LabelFrame(parent, text="1. Python Packages", padding="10")
        frame.pack(fill="x", pady=10)
        
        ttk.Label(frame, text="Required packages: requests, feedparser, python-dotenv, undetected-chromedriver, selenium").pack(anchor="w")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=5)
        
        self.package_status = ttk.Label(button_frame, text="Checking...")
        self.package_status.pack(side="left")
        
        ttk.Button(button_frame, text="Check Packages", command=self.check_packages).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Install Packages", command=self.install_packages).pack(side="right")

    def create_chrome_section(self, parent):
        frame = ttk.LabelFrame(parent, text="2. Chrome Browser & ChromeDriver", padding="10")
        frame.pack(fill="x", pady=10)
        
        ttk.Label(frame, text="Chrome browser is required for web scraping functionality.").pack(anchor="w")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=5)
        
        self.chrome_status = ttk.Label(button_frame, text="Checking...")
        self.chrome_status.pack(side="left")
        
        ttk.Button(button_frame, text="Check Chrome", command=self.check_chrome).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Download Chrome", command=self.download_chrome).pack(side="right")

    def create_env_section(self, parent):
        frame = ttk.LabelFrame(parent, text="3. Environment Variables (Slack Integration)", padding="10")
        frame.pack(fill="x", pady=10)
        
        ttk.Label(frame, text="Configure Slack webhook URLs for notifications (optional but recommended):").pack(anchor="w", pady=5)
        
        # Main webhook
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill="x", pady=2)
        ttk.Label(main_frame, text="Main Slack Webhook:").pack(side="left")
        self.main_webhook_var = tk.StringVar(value=os.getenv('MARADMIN_SLACK_WEBHOOK_URL', ''))
        ttk.Entry(main_frame, textvariable=self.main_webhook_var, width=50).pack(side="right", padx=5)
        
        # Delta webhook
        delta_frame = ttk.Frame(frame)
        delta_frame.pack(fill="x", pady=2)
        ttk.Label(delta_frame, text="Delta Group Webhook:").pack(side="left")
        self.delta_webhook_var = tk.StringVar(value=os.getenv('DELTA_SLACK_WEBHOOK_URL', ''))
        ttk.Entry(delta_frame, textvariable=self.delta_webhook_var, width=50).pack(side="right", padx=5)
        
        # MFCC webhook
        mfcc_frame = ttk.Frame(frame)
        mfcc_frame.pack(fill="x", pady=2)
        ttk.Label(mfcc_frame, text="MFCC Group Webhook:").pack(side="left")
        self.mfcc_webhook_var = tk.StringVar(value=os.getenv('MFCC_SLACK_WEBHOOK_URL', ''))
        ttk.Entry(mfcc_frame, textvariable=self.mfcc_webhook_var, width=50).pack(side="right", padx=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        self.env_status = ttk.Label(button_frame, text="")
        self.env_status.pack(side="left")
        
        ttk.Button(button_frame, text="Save Environment Variables", command=self.save_env_variables).pack(side="right")

    def create_csv_section(self, parent):
        frame = ttk.LabelFrame(parent, text="4. CSV Files Setup", padding="10")
        frame.pack(fill="x", pady=10)
        
        ttk.Label(frame, text="Required CSV files for the application:").pack(anchor="w", pady=5)
        
        # Contacts CSV
        contacts_frame = ttk.Frame(frame)
        contacts_frame.pack(fill="x", pady=2)
        ttk.Label(contacts_frame, text="Contacts CSV (contacts.csv):").pack(side="left")
        ttk.Button(contacts_frame, text="Create Template", command=self.create_contacts_template).pack(side="right", padx=5)
        ttk.Button(contacts_frame, text="Browse Existing", command=self.browse_contacts).pack(side="right")
        
        # MCC Codes CSV
        mcc_frame = ttk.Frame(frame)
        mcc_frame.pack(fill="x", pady=2)
        ttk.Label(mcc_frame, text="MCC Codes CSV (MCC Codes.csv):").pack(side="left")
        ttk.Button(mcc_frame, text="Create Template", command=self.create_mcc_template).pack(side="right", padx=5)
        ttk.Button(mcc_frame, text="Browse Existing", command=self.browse_mcc).pack(side="right")
        
        self.csv_status = ttk.Label(frame, text="")
        self.csv_status.pack(pady=5)
        
        ttk.Button(frame, text="Check CSV Files", command=self.check_csv_files).pack()

    def check_packages(self):
        try:
            with open('requirements.txt', 'r') as f:
                required_packages = [line.strip() for line in f if line.strip()]
            
            missing_packages = []
            for package in required_packages:
                try:
                    __import__(package.replace('-', '_'))
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                self.package_status.config(text=f"Missing: {', '.join(missing_packages)}", foreground="red")
                self.setup_steps["python_packages"] = False
            else:
                self.package_status.config(text="All packages installed ✓", foreground="green")
                self.setup_steps["python_packages"] = True
                
        except Exception as e:
            self.package_status.config(text=f"Error checking packages: {str(e)}", foreground="red")
            self.setup_steps["python_packages"] = False
        
        self.update_final_button()

    def install_packages(self):
        try:
            self.package_status.config(text="Installing packages...", foreground="blue")
            self.root.update()
            
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.package_status.config(text="Packages installed successfully ✓", foreground="green")
                self.setup_steps["python_packages"] = True
                messagebox.showinfo("Success", "All packages installed successfully!")
            else:
                self.package_status.config(text="Installation failed", foreground="red")
                messagebox.showerror("Error", f"Package installation failed:\n{result.stderr}")
                
        except Exception as e:
            self.package_status.config(text="Installation error", foreground="red")
            messagebox.showerror("Error", f"Error installing packages: {str(e)}")
        
        self.update_final_button()

    def check_chrome(self):
        try:
            # Check if Chrome is installed
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser"
            ]
            
            chrome_found = any(os.path.exists(path) for path in chrome_paths)
            
            if chrome_found:
                self.chrome_status.config(text="Chrome browser found ✓", foreground="green")
                self.setup_steps["chrome_driver"] = True
            else:
                self.chrome_status.config(text="Chrome browser not found", foreground="red")
                self.setup_steps["chrome_driver"] = False
                
        except Exception as e:
            self.chrome_status.config(text=f"Error checking Chrome: {str(e)}", foreground="red")
            self.setup_steps["chrome_driver"] = False
        
        self.update_final_button()

    def download_chrome(self):
        chrome_url = "https://www.google.com/chrome/"
        messagebox.showinfo("Download Chrome", 
                           f"Please download and install Chrome from:\n{chrome_url}\n\n"
                           "After installation, click 'Check Chrome' again.")
        
        # Try to open the URL in default browser
        try:
            import webbrowser
            webbrowser.open(chrome_url)
        except:
            pass

    def save_env_variables(self):
        try:
            env_file = Path('.env')
            env_vars = {}
            
            # Read existing .env file if it exists
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env_vars[key] = value
            
            # Update with new values
            if self.main_webhook_var.get().strip():
                env_vars['MARADMIN_SLACK_WEBHOOK_URL'] = self.main_webhook_var.get().strip()
            if self.delta_webhook_var.get().strip():
                env_vars['DELTA_SLACK_WEBHOOK_URL'] = self.delta_webhook_var.get().strip()
            if self.mfcc_webhook_var.get().strip():
                env_vars['MFCC_SLACK_WEBHOOK_URL'] = self.mfcc_webhook_var.get().strip()
            
            # Write back to .env file
            with open(env_file, 'w') as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            
            self.env_status.config(text="Environment variables saved ✓", foreground="green")
            self.setup_steps["env_variables"] = True
            messagebox.showinfo("Success", "Environment variables saved to .env file!")
            
        except Exception as e:
            self.env_status.config(text="Error saving variables", foreground="red")
            messagebox.showerror("Error", f"Error saving environment variables: {str(e)}")
        
        self.update_final_button()

    def create_contacts_template(self):
        try:
            template_data = [
                ['first_name', 'last_name', 'group', 'mos'],
                ['John', 'Doe', 'Personal', '0311'],
                ['Jane', 'Smith', 'Delta', '0651'],
                ['Bob', 'Johnson', 'MFCC', '0231']
            ]
            
            with open('contacts.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(template_data)
            
            messagebox.showinfo("Success", "Template contacts.csv created!\n\n"
                               "Please edit this file to add your actual contacts.")
            self.check_csv_files()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating contacts template: {str(e)}")

    def browse_contacts(self):
        filename = filedialog.askopenfilename(
            title="Select Contacts CSV File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filename:
            try:
                shutil.copy2(filename, 'contacts.csv')
                messagebox.showinfo("Success", "Contacts file copied successfully!")
                self.check_csv_files()
            except Exception as e:
                messagebox.showerror("Error", f"Error copying contacts file: {str(e)}")

    def create_mcc_template(self):
        try:
            template_data = [
                ['Code', 'Command', 'Location', 'Full_Name'],
                ['HQMC', 'Headquarters Marine Corps', 'Washington DC', 'Headquarters Marine Corps'],
                ['MCRD', 'Marine Corps Recruit Depot', 'Parris Island/San Diego', 'Marine Corps Recruit Depot'],
                ['MCB', 'Marine Corps Base', 'Various', 'Marine Corps Base']
            ]
            
            with open('MCC Codes.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(template_data)
            
            messagebox.showinfo("Success", "Template MCC Codes.csv created!\n\n"
                               "Please edit this file to add actual MCC codes.")
            self.check_csv_files()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating MCC template: {str(e)}")

    def browse_mcc(self):
        filename = filedialog.askopenfilename(
            title="Select MCC Codes CSV File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filename:
            try:
                shutil.copy2(filename, 'MCC Codes.csv')
                messagebox.showinfo("Success", "MCC Codes file copied successfully!")
                self.check_csv_files()
            except Exception as e:
                messagebox.showerror("Error", f"Error copying MCC codes file: {str(e)}")

    def check_csv_files(self):
        contacts_exists = Path('contacts.csv').exists()
        mcc_exists = Path('MCC Codes.csv').exists()
        
        if contacts_exists and mcc_exists:
            self.csv_status.config(text="All CSV files present ✓", foreground="green")
            self.setup_steps["csv_files"] = True
        elif contacts_exists:
            self.csv_status.config(text="Missing: MCC Codes.csv", foreground="orange")
            self.setup_steps["csv_files"] = False
        elif mcc_exists:
            self.csv_status.config(text="Missing: contacts.csv", foreground="orange")
            self.setup_steps["csv_files"] = False
        else:
            self.csv_status.config(text="Missing: contacts.csv, MCC Codes.csv", foreground="red")
            self.setup_steps["csv_files"] = False
        
        self.update_final_button()

    def check_all_status(self):
        self.check_packages()
        self.check_chrome()
        self.check_csv_files()
        
        # Check env variables
        if (os.getenv('MARADMIN_SLACK_WEBHOOK_URL') or 
            os.getenv('DELTA_SLACK_WEBHOOK_URL') or 
            os.getenv('MFCC_SLACK_WEBHOOK_URL')):
            self.env_status.config(text="Environment variables configured ✓", foreground="green")
            self.setup_steps["env_variables"] = True
        else:
            self.env_status.config(text="No environment variables set (optional)", foreground="orange")
            self.setup_steps["env_variables"] = True  # Make this optional

    def update_final_button(self):
        if all(self.setup_steps.values()):
            self.final_button.config(state="normal")
            self.status_label.config(text="Ready to complete setup!", foreground="green")
        else:
            self.final_button.config(state="disabled")
            missing = [k for k, v in self.setup_steps.items() if not v]
            self.status_label.config(text=f"Complete remaining steps: {', '.join(missing)}", foreground="red")

    def complete_setup(self):
        try:
            # Test the setup by importing the main processor
            from maradmin_processor import MaradminProcessor
            
            # Try to initialize it
            processor = MaradminProcessor()
            
            # Create logs directory if it doesn't exist
            Path('logs').mkdir(exist_ok=True)
            
            messagebox.showinfo("Setup Complete!", 
                               "Environment setup completed successfully!\n\n"
                               "You can now run the main application using:\n"
                               "- python main.py (for command line)\n"
                               "- python run_gui.py (for GUI)")
            
            # Ask if user wants to run the GUI now
            if messagebox.askyesno("Run Application", "Would you like to run the GUI application now?"):
                self.root.destroy()
                # Import and run the main GUI
                from gui import MaradminGUI
                root = tk.Tk()
                app = MaradminGUI(root)
                root.mainloop()
            else:
                self.root.destroy()
                
        except Exception as e:
            messagebox.showerror("Setup Test Failed", 
                               f"Setup test failed: {str(e)}\n\n"
                               "Please check your configuration and try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvironmentSetupGUI(root)
    root.mainloop()
