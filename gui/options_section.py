import tkinter as tk
from tkinter import ttk

class OptionsSection:
    def __init__(self, parent, save_tokens_to_env_command):
        self.parent = parent
        self.save_tokens_to_env_command = save_tokens_to_env_command
        self.create_options_section()

    def create_options_section(self):
        """Creates the options section"""
        options_frame = ttk.LabelFrame(self.parent, text="Opções", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Save config checkbox
        self.save_config_var = tk.BooleanVar()
        self.save_config_check = ttk.Checkbutton(
            options_frame,
            text="Salvar configurações no arquivo .env",
            variable=self.save_config_var
        )
        self.save_config_check.grid(row=0, column=0, sticky=tk.W)

        # Save config button
        self.save_config_button = ttk.Button(
            options_frame,
            text="Salvar Tokens",
            command=self.save_tokens_to_env_command
        )
        self.save_config_button.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.save_config_check.grid(row=0, column=0, sticky=tk.W)

        # Skip existing repos checkbox
        self.skip_existing_var = tk.BooleanVar()
        self.skip_existing_check = ttk.Checkbutton(
            options_frame,
            text="Pular repositórios já processados",
            variable=self.skip_existing_var
        )
        self.skip_existing_check.grid(row=1, column=0, sticky=tk.W)

        # Retry count
        ttk.Label(options_frame, text="Número de tentativas:").grid(row=2, column=0, sticky=tk.W)
        self.retry_count = ttk.Spinbox(options_frame, from_=1, to=5, width=5)
        self.retry_count.grid(row=2, column=1, sticky=tk.W)
        self.retry_count.set(3)

        # Repository limit
        ttk.Label(options_frame, text="Número de repositórios para backup (deixe em branco para todos):").grid(row=3, column=0, sticky=tk.W)
        self.repo_limit_spinbox = ttk.Spinbox(options_frame, from_=1, to=1000, width=5) # Assuming max 1000 repos is reasonable
        self.repo_limit_spinbox.grid(row=3, column=1, sticky=tk.W)

    def get_save_config_var(self):
        return self.save_config_var.get()

    def get_skip_existing_var(self):
        return self.skip_existing_var.get()

    def get_retry_count(self):
        return int(self.retry_count.get())

    def get_repo_limit(self):
        limit_str = self.repo_limit_spinbox.get().strip()
        if limit_str:
            return int(limit_str)
        return None  # Return None if the field is left blank
