import pandas as pd
import os
from pathlib import Path
from tkinter import messagebox
from typing import List, Tuple

def load_data(files_to_upload: List[Tuple[str, int, str]], required_files: List[str], output_dir: Path) -> dict:
    data = {}
    for file_name in required_files:
        file_path = None
        
        for name, _, path in files_to_upload:
            if name == file_name:
                file_path = path
                break
        
        if not file_path:
            converted_path = output_dir / file_name
            if converted_path.exists():
                file_path = converted_path
        
        if file_path:
            try:
                data[file_name.replace('.csv', '')] = pd.read_csv(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load {file_name}: {str(e)}")
                return None
        else:
            messagebox.showerror("Error", f"Missing required file: {file_name}")
            return None
    
    return data

def convert_excel_to_csv(file_path: str, output_dir: Path) -> List[str]:
    try:
        excel_data = pd.ExcelFile(file_path, engine="openpyxl")
        converted_files = []
        
        for sheet_name in excel_data.sheet_names:
            df = excel_data.parse(sheet_name)
            csv_file_name = output_dir / f"{sheet_name}.csv"
            df.to_csv(csv_file_name, index=False)
            converted_files.append(csv_file_name.name)
        
        return converted_files
    except Exception as e:
        raise Exception(f"Error converting {file_path} to CSV: {str(e)}")

def check_required_files(files_to_upload: List[Tuple[str, int, str]], required_files: List[str], output_dir: Path) -> bool:
    existing_files = {name for name, _, _ in files_to_upload}
    if output_dir.exists():
        existing_files.update(f.name for f in output_dir.glob('*.csv'))
    
    missing_files = set(required_files) - existing_files
    if missing_files:
        messagebox.showerror(
            "Missing Files",
            f"The following required files are missing:\n{', '.join(missing_files)}"
        )
        return False
    
    return True
