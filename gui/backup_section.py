import tkinter as tk
from tkinter import ttk, filedialog

class BackupSection:
    def __init__(self, parent, browse_directory_command):
        self.parent = parent
        self.browse_directory_command = browse_directory_command
        self.create_backup_section()

    def create_backup_section(self):
        """Creates the backup directory section"""
        backup_frame = ttk.LabelFrame(self.parent, text="Configurações de Backup", padding="10")
        backup_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(backup_frame, text="Diretório:").grid(row=0, column=0, sticky=tk.W)
        self.backup_dir_entry = ttk.Entry(backup_frame, width=60)
        self.backup_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        browse_button = ttk.Button(backup_frame, text="Procurar", command=self.browse_directory_command)
        browse_button.grid(row=0, column=2, padx=5)

    def get_backup_dir(self):
        return self.backup_dir_entry.get().strip()
