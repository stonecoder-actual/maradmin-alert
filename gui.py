import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from pathlib import Path
from maradmin_processor import MaradminProcessor

class MaradminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MARADMIN Alert GUI")
        self.root.geometry("800x600")
        
        self.processor = MaradminProcessor()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # CSV File Selection
        ttk.Label(main_frame, text="Contacts CSV File:").grid(row=0, column=0, sticky=tk.W)
        self.csv_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.csv_path_var, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_csv).grid(row=0, column=2)
        
        # Name Input Fields
        ttk.Label(main_frame, text="First Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.first_name_var).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Last Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.last_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.last_name_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Promotion Type Dropdown
        ttk.Label(main_frame, text="Promotion Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.promotion_type = tk.StringVar()
        promotion_combo = ttk.Combobox(main_frame, textvariable=self.promotion_type)
        promotion_combo['values'] = ('Officer', 'Enlisted')
        promotion_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        promotion_combo.set('Officer')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Search", command=self.search_maradmins).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Processed MARADMINs", command=self.clear_processed).pack(side=tk.LEFT, padx=5)
        
        # Results Area
        ttk.Label(main_frame, text="Results:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.results_text = tk.Text(main_frame, height=20, width=80)
        self.results_text.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S))
        self.results_text['yscrollcommand'] = scrollbar.set

    def browse_csv(self):
        filename = filedialog.askopenfilename(
            title="Select Contacts CSV File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filename:
            self.csv_path_var.set(filename)

    def search_maradmins(self):
        try:
            first_name = self.first_name_var.get().strip()
            last_name = self.last_name_var.get().strip()
            
            if not first_name or not last_name:
                messagebox.showerror("Error", "Please enter both first and last name")
                return
                
            csv_path = self.csv_path_var.get()
            if not csv_path:
                messagebox.showerror("Error", "Please select a contacts CSV file")
                return
                
            if not Path(csv_path).exists():
                messagebox.showerror("Error", "Selected CSV file does not exist")
                return

            # Create a single contact for search
            contact = {
                'first_name': first_name.upper(),
                'last_name': last_name.upper(),
                'full_name': f"{last_name.upper()}, {first_name.upper()}",
                'group': 'Personal'
            }
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Searching for: {contact['full_name']}\n")
            self.results_text.insert(tk.END, "Initializing search...\n")
            self.root.update()
            
            # Update processor with custom CSV path and single contact
            self.processor.config = dict(self.processor.config)
            self.processor.config['contacts_file'] = csv_path
            self.processor.contacts = [contact]  # Set single contact for search
            
            try:
                # Initialize the processor
                self.processor.setup_driver()
                
                # Get all MARADMINs (not just new ones for single user search)
                self.results_text.insert(tk.END, "Checking RSS feed for MARADMINs...\n")
                self.root.update()
                
                # Get all entries regardless of processed status for single user search
                import feedparser
                feed = feedparser.parse(self.processor.config['rss_url'])
                all_entries = []
                
                promotion_type = self.promotion_type.get()
                if promotion_type == "Officer":
                    target_titles = self.processor.config['officer_promotion_titles']
                else:
                    target_titles = self.processor.config['enlisted_promotion_titles']
                
                for entry in feed.entries:
                    if any(title in entry.title.upper() for title in target_titles):
                        all_entries.append(entry)
                
                if not all_entries:
                    self.results_text.insert(tk.END, f"No {promotion_type.lower()} promotion MARADMINs found in feed.\n")
                    return
                    
                self.results_text.insert(tk.END, f"Found {len(all_entries)} {promotion_type.lower()} promotion MARADMINs to search...\n\n")
                self.root.update()
                
                found_matches = False
                for entry in all_entries:
                    self.results_text.insert(tk.END, f"Processing: {entry['title']}\n")
                    self.root.update()
                    
                    # Process with single contact
                    page_text = self.processor.extract_page_text(entry['link'])
                    if page_text:
                        if promotion_type == "Officer":
                            matches = self.processor.search_1stlt_promotions(page_text, [contact])
                        else:
                            matches = self.processor.search_enlisted_promotions(page_text, [contact])
                        
                        if matches:
                            found_matches = True
                            self.results_text.insert(tk.END, f"\n*** MATCH FOUND! ***\n")
                            self.results_text.insert(tk.END, f"MARADMIN: {entry['title']}\n")
                            self.results_text.insert(tk.END, f"Link: {entry['link']}\n")
                            self.results_text.insert(tk.END, "Matches:\n")
                            for match in matches:
                                self.results_text.insert(tk.END, f"- {match['name_format']}\n")
                                if 'matched_text' in match:
                                    self.results_text.insert(tk.END, f"  Found in text: {match['matched_text']}\n")
                            self.results_text.insert(tk.END, "\n")
                            self.root.update()
                
                if not found_matches:
                    self.results_text.insert(tk.END, f"\nNo matches found for {contact['full_name']} in any {promotion_type.lower()} promotion MARADMINs.\n")
                    
            except Exception as e:
                self.results_text.insert(tk.END, f"\nError during processing: {str(e)}\n")
                messagebox.showerror("Processing Error", f"An error occurred while processing MARADMINs: {str(e)}")
            finally:
                self.processor.cleanup_driver()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_processed(self):
        try:
            # Clear the processed_maradmins.json file
            with open(self.processor.config['archive_file'], 'w') as f:
                json.dump({}, f)
            self.processor.processed_maradmins = {}
            messagebox.showinfo("Success", "Processed MARADMINs have been cleared.")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Processed MARADMINs have been cleared.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear processed MARADMINs: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MaradminGUI(root)
    root.mainloop()
