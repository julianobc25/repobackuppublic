import tkinter as tk
from tkinter import ttk, scrolledtext

class BackupGUIComponents:
    def __init__(self, root):
        self.root = root
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Origem (Primeira conta)
        ttk.Label(self.main_frame, text="Conta de Origem:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.main_frame, text="Token:").grid(row=1, column=0, sticky=tk.W)
        self.source_token_entry = ttk.Entry(self.main_frame, width=50)
        self.source_token_entry.grid(row=1, column=1, sticky=tk.W)

        # Destino (Segunda conta)
        ttk.Label(self.main_frame, text="Conta de Destino:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.main_frame, text="Token:").grid(row=3, column=0, sticky=tk.W)
        self.dest_token_entry = ttk.Entry(self.main_frame, width=50)
        self.dest_token_entry.grid(row=3, column=1, sticky=tk.W)

        # Diretório de backup
        ttk.Label(self.main_frame, text="Diretório de Backup:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.backup_dir_entry = ttk.Entry(self.main_frame, width=50)
        self.backup_dir_entry.grid(row=4, column=1, sticky=tk.W)

        # Checkbox para salvar configurações
        self.save_config_var = tk.BooleanVar()
        self.save_config_check = ttk.Checkbutton(
            self.main_frame,
            text="Salvar configurações no arquivo .env",
            variable=self.save_config_var
        )
        self.save_config_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Área de status
        ttk.Label(self.main_frame, text="Status:", font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.status_area = scrolledtext.ScrolledText(self.main_frame, width=70, height=20)
        self.status_area.grid(row=7, column=0, columnspan=2, pady=5)

        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, length=600, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=8, column=0, columnspan=2, pady=5)

        # Botões
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Iniciar Backup")
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(self.button_frame, text="Pausar", state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)