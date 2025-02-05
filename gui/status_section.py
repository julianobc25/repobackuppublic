import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class StatusSection:
    def __init__(self, parent):
        self.parent = parent
        self.status_area = None  # Initialize status_area
        self.progress_var = None # Initialize progress_var
        self.progress_bar = None # Initialize progress_bar
        self.progress_label = None # Initialize progress_label
        self.create_status_section()

    def create_status_section(self):
        """Creates the status section"""
        status_frame = ttk.LabelFrame(self.parent, text="Status", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Status area
        self.status_area = scrolledtext.ScrolledText(status_frame, width=70, height=15)
        self.status_area.grid(row=0, column=0, columnspan=2, pady=5)

        # Progress section
        progress_frame = ttk.Frame(status_frame)
        progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(side=tk.LEFT, padx=(0, 10))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=600,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_progress(self, value, text=None):
        """Updates progress bar and label"""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=f"{int(value)}% - {text}")
        else:
            self.progress_label.config(text=f"{int(value)}%")

    def add_status_message(self, message, message_type="info"):
        """Adds message to status area with color coding"""
        tags = {
            "info": "black",
            "success": "green",
            "error": "red",
            "warning": "orange"
        }

        self.status_area.tag_config("timestamp", foreground="blue")
        self.status_area.tag_config(message_type, foreground=tags.get(message_type, "black"))

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.status_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.status_area.insert(tk.END, f"{message}\n", message_type)
        self.status_area.see(tk.END)  # Auto-scroll to bottom

    def clear_status(self):
        """Clears the status area"""
        self.status_area.delete(1.0, tk.END)
