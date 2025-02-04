import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from ttkthemes import ThemedTk
from backup_logic.token_validation import validate_tokens as validate_github_tokens
from github import Github

class BackupGUIComponents:
    def __init__(self, root, logger=None, error_logger=None):
        self.root = root
        self.logger = logger
        self.error_logger = error_logger
        if isinstance(root, ThemedTk):
            self.root.set_theme("arc")  # Modern theme

        self.root.title("GitHub Repository Backup Tool")
        self.root.geometry("800x700")  # Larger window
        
        # Configure style
        style = ttk.Style()
        style.configure("Title.TLabel", font=('Helvetica', 14, 'bold'))
        style.configure("Header.TLabel", font=('Helvetica', 11, 'bold'))
        style.configure("Success.TLabel", foreground="green")
        style.configure("Error.TLabel", foreground="red")
        
        self.create_main_frame()
        self.create_token_section()
        self.create_backup_section()
        self.create_options_section()
        self.create_status_section()
        self.create_control_section()

    def create_main_frame(self):
        """Create and configure the main frame"""
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(1, weight=1)

        # Title
        title = ttk.Label(self.main_frame, text="GitHub Repository Backup Tool", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    def create_token_section(self):
        """Create the token input section"""
        # Source Account Frame
        source_frame = ttk.LabelFrame(self.main_frame, text="Conta de Origem", padding="10")
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
                                             command=self.refresh_repo_count)
        self.refresh_count_button.pack(side=tk.LEFT)
        
        # Destination Account Frame
        dest_frame = ttk.LabelFrame(self.main_frame, text="Conta de Destino", padding="10")
        dest_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(dest_frame, text="Token:").grid(row=0, column=0, sticky=tk.W)
        self.dest_token_entry = ttk.Entry(dest_frame, width=70)
        self.dest_token_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

    def create_backup_section(self):
        """Create the backup directory section"""
        backup_frame = ttk.LabelFrame(self.main_frame, text="Configurações de Backup", padding="10")
        backup_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(backup_frame, text="Diretório:").grid(row=0, column=0, sticky=tk.W)
        self.backup_dir_entry = ttk.Entry(backup_frame, width=60)
        self.backup_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        browse_button = ttk.Button(backup_frame, text="Procurar", command=self.browse_directory)
        browse_button.grid(row=0, column=2, padx=5)

    def create_options_section(self):
        """Create the options section"""
        options_frame = ttk.LabelFrame(self.main_frame, text="Opções", padding="10")
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
            command=self.save_tokens_to_env
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

    def create_status_section(self):
        """Create the status section"""
        status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="10")
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

    def create_control_section(self):
        """Create the control buttons section"""
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Validation button
        self.validate_button = ttk.Button(control_frame, text="Validar Tokens", command=self.validate_tokens)
        self.validate_button.pack(side=tk.LEFT, padx=5)
        
        # Start button
        self.start_button = ttk.Button(control_frame, text="Iniciar Backup")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Pause button
        self.pause_button = ttk.Button(control_frame, text="Pausar", state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        self.cancel_button = ttk.Button(control_frame, text="Cancelar", state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def validate_tokens(self):
        """Validate both source and destination GitHub tokens"""
        source_token = self.source_token_entry.get().strip()
        dest_token = self.dest_token_entry.get().strip()

        if not source_token or not dest_token:
            self.add_status_message("Erro: Ambos os tokens são necessários", "error")
            return

        try:
            self.add_status_message("Validando tokens...", "info")
            if validate_github_tokens(source_token, dest_token, self.logger, self.error_logger):
                self.add_status_message("Tokens validados com sucesso!", "success")
                self.show_success("Sucesso", "Ambos os tokens são válidos e têm as permissões necessárias")
            else:
                self.add_status_message("Erro na validação dos tokens", "error")
                self.show_error("Erro", "Um ou mais tokens são inválidos ou não têm permissões suficientes")
        except Exception as e:
            error_msg = str(e)
            self.add_status_message(f"Erro: {error_msg}", "error")
            self.show_error("Erro na Validação", error_msg)
            if self.error_logger:
                self.error_logger.log_error(Exception(error_msg), "Token validation error")

    def save_tokens_to_env(self):
        source_token = self.source_token_entry.get().strip()
        dest_token = self.dest_token_entry.get().strip()
        backup_dir = self.backup_dir_entry.get().strip()

        if not source_token or not dest_token or not backup_dir:
            self.add_status_message("Erro: Todos os campos são obrigatórios", "error")
            return

        with open('.env', 'w') as f:
            f.write(f"SOURCE_GITHUB_TOKEN={source_token}\n")
            f.write(f"DEST_GITHUB_TOKEN={dest_token}\n")
            f.write(f"BACKUP_DIR={backup_dir}\n")
        self.add_status_message("Tokens salvos no arquivo .env", "success")

    def browse_directory(self):
        """Open directory browser dialog"""
        directory = filedialog.askdirectory(
            title="Selecione o diretório de backup",
            initialdir="."
        )
        if directory:
            self.backup_dir_entry.delete(0, tk.END)
            self.backup_dir_entry.insert(0, directory)

    def update_progress(self, value, text=None):
        """Update progress bar and label"""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=f"{int(value)}% - {text}")
        else:
            self.progress_label.config(text=f"{int(value)}%")

    def add_status_message(self, message, message_type="info"):
        """Add message to status area with color coding"""
        tags = {
            "info": "black",
            "success": "green",
            "error": "red",
            "warning": "orange"
        }
        
        self.status_area.tag_config("timestamp", foreground="blue")
        self.status_area.tag_config(message_type, foreground=tags.get(message_type, "black"))
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.status_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.status_area.insert(tk.END, f"{message}\n", message_type)
        self.status_area.see(tk.END)  # Auto-scroll to bottom

    def clear_status(self):
        """Clear the status area"""
        self.status_area.delete(1.0, tk.END)
        
    def show_error(self, title, message):
        """Show error message box"""
        messagebox.showerror(title, message)
        
    def show_success(self, title, message):
        """Show success message box"""
        messagebox.showinfo(title, message)

    def refresh_repo_count(self):
        """Refresh the repository count for the source account"""
        source_token = self.source_token_entry.get().strip()
        
        if not source_token:
            self.add_status_message("Erro: Token de origem é necessário", "error")
            self.repo_count_label.config(text="Repositórios: -")
            return
            
        try:
            try:
                # Try to ping GitHub API first to check connectivity
                import socket
                socket.create_connection(("api.github.com", 443), timeout=5)
                
                # Create a GitHub client and get repository count
                g = Github(source_token)
                user = g.get_user()
                repos = list(user.get_repos())
                count = len(repos)
                self.repo_count_label.config(text=f"Repositórios: {count}")
                self.add_status_message(f"Contagem atualizada: {count} repositórios encontrados", "success")
            except socket.error:
                raise Exception("Não foi possível conectar ao GitHub. Verifique sua conexão com a internet.")
        except Exception as e:
            error_msg = f"Erro ao obter contagem: {str(e)}"
            self.add_status_message(error_msg, "error")
            self.repo_count_label.config(text="Repositórios: -")