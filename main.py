import tkinter as tk
from ui.drag_drop_ui import DragDropUploadUI

def main():
    root = tk.Tk()
    app = DragDropUploadUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
