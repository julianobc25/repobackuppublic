import tkinter as tk
from tkinter import ttk
from github import Github

class TokenSection:
    def __init__(self, parent, refresh_repo_count_command):
        self.parent = parent
        self.refresh_repo_count_command = refresh_repo_count_command
        self.create_token_section()

    def create_token_section(self):
        """Creates the token input section"""
        # Source Account Frame
        source_frame = ttk.LabelFrame(self.parent, text="Conta de Origem", padding="10")
        source_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(source_frame, text="Token:").grid(row=0, column=0, sticky=tk.W)
        self.source_token_entry = ttk.Entry(source_frame, width=70)
        self.source_token_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # Repository count refresh button and label
        refresh_frame = ttk.Frame(source_frame)
        refresh_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        self.repo_count_label = ttk.Label(refresh_frame, text="Repositórios: -")
        self.repo_count_label.pack(side=tk.LEFT, padx=(0, 10))

        self.refresh_count_button = ttk.Button(refresh_frame, text="Atualizar Contagem",
                                             command=self.refresh_repo_count_command)
        self.refresh_count_button.pack(side=tk.LEFT)

        # Destination Account Frame
        dest_frame = ttk.LabelFrame(self.parent, text="Conta de Destino", padding="10")
        dest_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(dest_frame, text="Token:").grid(row=0, column=0, sticky=tk.W)
        self.dest_token_entry = ttk.Entry(dest_frame, width=70)
        self.dest_token_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

    def get_source_token(self):
        return self.source_token_entry.get().strip()

    def get_dest_token(self):
        return self.dest_token_entry.get().strip()

    def set_repo_count_label(self, text):
        self.repo_count_label.config(text=text)
