import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox
from pathlib import Path
from typing import List, Tuple
import threading
from utils.ops import browse_files, validate_file_type, simulate_upload
from utils.processing import load_data, check_required_files, convert_excel_to_csv
from utils.report import create_portfolio_reports

class DragDropUploadUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Analysis Tool")
        self.root.geometry("600x400")
        self.accepted_types = {
            'Excel files': ('*.xlsx', '*.xls', '*.xlsm'),
            'CSV files': ('*.csv',)
        }
        self.required_files = [
            'Portfolio Value.csv', 'Holding.csv', 'XIRR.csv', 
            'Equity.csv', 'Debt.csv', 'FNO.csv', 'Profits.csv'
        ]
        self.files_to_upload: List[Tuple[str, int, str]] = []
        self.desktop_path = Path.home() / "Desktop"
        self.output_dir = self.desktop_path / "converted_files"
        self.output_dir.mkdir(exist_ok=True)
        self.portfolio_dir = self.desktop_path / "portfolio_reports"
        self.portfolio_dir.mkdir(exist_ok=True)
        self.setup_ui()

    def setup_ui(self):
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        self.create_upload_interface()
        
    def create_upload_interface(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        self.drop_frame = ttk.Frame(self.main_container, borderwidth=2, relief="solid")
        self.drop_frame.pack(fill=tk.X, pady=(0, 20))
        
        upload_frame = ttk.Frame(self.drop_frame)
        upload_frame.pack(pady=20)
        
        upload_icon = ttk.Label(upload_frame, text="↑")
        upload_icon.pack()
        
        upload_label = ttk.Label(
            upload_frame,
            text="Drag and drop files here or upload",
            font=('Arial', 11)
        )
        upload_label.pack()

        file_types = ttk.Label(
            self.drop_frame,
            text="Accepted file types: Excel (.xlsx, .xls, .xlsm), CSV (.csv)",
            foreground="gray"
        )
        file_types.pack(pady=(0, 10))

        upload_btn = ttk.Button(
            self.drop_frame,
            text="Upload",
            command=self.browse_files
        )
        upload_btn.pack(pady=(0, 20))

        self.files_counter = ttk.Label(
            self.main_container,
            text="0 of 7 files uploaded"
        )
        self.files_counter.pack(anchor=tk.W, pady=(0, 10))

        self.files_frame = ttk.Frame(self.main_container)
        self.files_frame.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(pady=(10, 0))

        self.convert_btn = ttk.Button(
            button_frame,
            text="Convert Files",
            command=self.process_files,
            state="disabled"
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)

        self.generate_btn = ttk.Button(
            button_frame,
            text="Generate",
            command=self.generate_files,
            state="disabled"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)

    def browse_files(self):
        files = browse_files(self.root, self.accepted_types)
        if files:
            self.add_files(files)

    def add_files(self, files):
        for file in files:
            if len(self.files_to_upload) >= 7:
                messagebox.showwarning("Limit Reached", "Maximum 7 files can be uploaded at once.")
                break
                
            if not validate_file_type(file):
                messagebox.showerror("Invalid File", f"File type not supported: {file}")
                continue
                
            filename = Path(file).name
            size = Path(file).stat().st_size // (1024 * 1024)
            
            file_frame = ttk.Frame(self.files_frame)
            file_frame.pack(fill=tk.X, pady=5)
            
            icon_text = "📊" if filename.endswith('.csv') else "📑"
            icon_label = ttk.Label(file_frame, text=icon_text)
            icon_label.pack(side=tk.LEFT, padx=5)
            
            name_label = ttk.Label(
                file_frame,
                text=f"{filename} {size} mb"
            )
            name_label.pack(side=tk.LEFT, padx=5)
            
            progress = ttk.Progressbar(
                file_frame,
                length=200,
                mode='determinate'
            )
            progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            
            cancel_btn = ttk.Button(
                file_frame,
                text="✕",
                width=3,
                command=lambda f=file_frame: self.remove_file(f)
            )
            cancel_btn.pack(side=tk.RIGHT, padx=5)
            
            self.files_to_upload.append((filename, size, file))
            self.update_counter()
            
            simulate_upload(progress, self.root)
        
        button_state = 'normal' if self.files_to_upload else 'disabled'
        self.convert_btn['state'] = button_state
        self.generate_btn['state'] = button_state

    def remove_file(self, file_frame):
        index = list(self.files_frame.children.values()).index(file_frame)
        self.files_to_upload.pop(index)
        file_frame.destroy()
        self.update_counter()
        button_state = 'normal' if self.files_to_upload else 'disabled'
        self.convert_btn['state'] = button_state
        self.generate_btn['state'] = button_state

    def update_counter(self):
        self.files_counter.configure(
            text=f"{len(self.files_to_upload)} of 7 files uploaded"
        )

    def process_files(self):
        self.convert_btn['state'] = 'disabled'
        self.generate_btn['state'] = 'disabled'
        
        def conversion_thread():
            converted_files = []
            for filename, _, file_path in self.files_to_upload:
                try:
                    if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                        converted = convert_excel_to_csv(file_path, self.output_dir)
                        converted_files.extend(converted)
                    else:
                        output_path = self.output_dir / filename
                        pd.read_csv(file_path).to_csv(output_path, index=False)
                        converted_files.append(filename)
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {filename}: {str(e)}")
                    continue
            
            messagebox.showinfo("Success", "Files have been processed successfully!")
            self.convert_btn['state'] = 'normal'
            self.generate_btn['state'] = 'normal'

        thread = threading.Thread(target=conversion_thread)
        thread.start()

    def generate_files(self):
        if not check_required_files(self.files_to_upload, self.required_files, self.output_dir):
            return

        self.generate_btn['state'] = 'disabled'
        self.convert_btn['state'] = 'disabled'

        progress_window = tk.Toplevel(self.root)
        progress_window.title("Generating Reports")
        progress_window.geometry("300x150")
        progress_window.transient(self.root)
    
        progress_label = ttk.Label(progress_window, text="Generating portfolio reports...")
        progress_label.pack(pady=20)
    
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(pady=10, padx=20, fill=tk.X)
        progress_bar.start()

        def generation_thread():
            try:
                data = load_data(self.files_to_upload, self.required_files, self.output_dir)
                if not data:
                    progress_window.destroy()
                    return

                self.root.after(0, lambda: self.create_reports_on_main_thread(data, progress_window))
            
            except Exception as e:
                def error_handler():
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error generating reports: {str(e)}")
                    self.reset_interface()
            
                self.root.after(0, error_handler)

        thread = threading.Thread(target=generation_thread)
        thread.start()

    def create_reports_on_main_thread(self, data, progress_window):
        try:
            create_portfolio_reports(data, self.portfolio_dir)
            progress_window.destroy()
            messagebox.showinfo(
                "Success", 
                f"Portfolio reports have been generated successfully in the '{self.portfolio_dir}' directory."
            )
            self.reset_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Error generating reports: {str(e)}")
            self.reset_interface()

    def reset_interface(self):
        self.files_to_upload = []
        self.create_upload_interface()
        self.root.update()
