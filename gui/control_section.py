import tkinter as tk
from tkinter import ttk

class ControlSection:
    def __init__(self, parent, validate_tokens_command, start_backup_command, pause_backup_command, cancel_backup_command):
        self.parent = parent
        self.validate_tokens_command = validate_tokens_command
        self.start_backup_command = start_backup_command
        self.pause_backup_command = pause_backup_command
        self.cancel_backup_command = cancel_backup_command
        self.create_control_section()

    def create_control_section(self):
        """Creates the control buttons section"""
        control_frame = ttk.Frame(self.parent)
        control_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Validation button
        self.validate_button = ttk.Button(control_frame, text="Validar Tokens", command=self.validate_tokens_command)
        self.validate_button.pack(side=tk.LEFT, padx=5)

        # Start button
        self.start_button = ttk.Button(control_frame, text="Iniciar Backup", command=self.start_backup_command)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Pause button
        self.pause_button = ttk.Button(control_frame, text="Pausar", state=tk.DISABLED, command=self.pause_backup_command)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Cancel button
        self.cancel_button = ttk.Button(control_frame, text="Cancelar", state=tk.DISABLED, command=self.cancel_backup_command)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
