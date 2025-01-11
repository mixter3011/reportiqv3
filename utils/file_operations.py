import threading
import time
import os
from tkinter import filedialog

def browse_files(root, accepted_types):
    filetypes = [(name, ' '.join(extensions)) for name, extensions in accepted_types.items()]
    filetypes.append(('All accepted files', ' '.join(sum(accepted_types.values(), ()))))
    return filedialog.askopenfilenames(parent=root, title="Select Files", filetypes=filetypes)

def validate_file_type(filename: str) -> bool:
    ext = os.path.splitext(filename.lower())[1]
    allowed_extensions = ('.xlsx', '.xls', '.xlsm', '.csv')
    return ext in allowed_extensions

def simulate_upload(progress_bar, root):

    def update_progress():
        for i in range(101):
            progress_bar['value'] = i
            time.sleep(0.05)
            root.update()

    thread = threading.Thread(target=update_progress)
    thread.start()

def create_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def get_file_size(filepath: str) -> float:
    return os.path.getsize(filepath) / (1024 * 1024)

def delete_file(filepath: str) -> None:
    if os.path.exists(filepath):
        os.remove(filepath)

def list_files_in_directory(directory: str, extensions: tuple = ()) -> list:
    if not os.path.exists(directory):
        return []
    return [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(extensions)
    ]
