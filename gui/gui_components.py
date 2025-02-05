import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from ttkthemes import ThemedTk
from backup_logic.token_validation import validate_tokens as validate_github_tokens
from github import Github

from .token_section import TokenSection
from .backup_section import BackupSection
from .options_section import OptionsSection
from .status_section import StatusSection
from .control_section import ControlSection


class BackupGUIComponents:
    def __init__(self, root, logger=None, error_logger=None):
        self.root = root
        self.logger = logger
        self.error_logger = error_logger
        if isinstance(root, ThemedTk):
            self.root.set_theme("arc")  # Modern theme

        self.root.title("GitHub Repository Backup Tool")
        self.root.geometry("700x850")  # Larger window, increased width to 850

        # Configure style
        style = ttk.Style()
        style.configure("Title.TLabel", font=('Helvetica', 14, 'bold'))
        style.configure("Header.TLabel", font=('Helvetica', 11, 'bold'))
        style.configure("Success.TLabel", foreground="green")
        style.configure("Error.TLabel", foreground="red")

        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(1, weight=1)

        # Title
        title = ttk.Label(self.main_frame, text="GitHub Repository Backup Tool", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.token_section = TokenSection(self.main_frame, self.refresh_repo_count)
        self.backup_section = BackupSection(self.main_frame, self.browse_directory) # Pass browse_directory command
        self.options_section = OptionsSection(self.main_frame, self.save_tokens_to_env)
        self.status_section = StatusSection(self.main_frame)
        self.control_section = ControlSection(
            self.main_frame, 
            self.validate_tokens,
            self.start_backup,
            self.pause_backup,
            self.cancel_backup
        )

    def set_repo_count_label(self, text):
        self.token_section.set_repo_count_label(text)

    def update_progress(self, value, text=None):
        self.status_section.update_progress(value, text)

    def add_status_message(self, message, message_type="info"):
        self.status_section.add_status_message(message, message_type)

    def clear_status(self):
        self.status_section.clear_status()

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_success(self, title, message):
        messagebox.showinfo(title, message)

    def get_source_token(self):
        return self.token_section.get_source_token()

    def get_dest_token(self):
        return self.token_section.get_dest_token()

    def get_backup_dir(self):
        return self.backup_section.get_backup_dir()

    def get_save_config_var(self):
        return self.options_section.get_save_config_var()

    def get_skip_existing_var(self):
        return self.options_section.get_skip_existing_var()

    def get_retry_count(self):
        return self.options_section.get_retry_count()
    
    def get_repo_limit(self):
        return self.options_section.get_repo_limit()

    def validate_tokens(self):
        """Validate tokens using token_validation.validate_tokens"""
        source_token = self.get_source_token()
        dest_token = self.get_dest_token()

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
        """Saves tokens to .env file"""
        source_token = self.get_source_token()
        dest_token = self.get_dest_token()
        backup_dir = self.get_backup_dir()

        if not source_token or not dest_token or not backup_dir:
            self.add_status_message("Erro: Todos os campos são obrigatórios", "error")
            return

        if self.get_save_config_var():
            with open('.env', 'w') as f:
                f.write(f"SOURCE_GITHUB_TOKEN={source_token}\n")
                f.write(f"DEST_GITHUB_TOKEN={dest_token}\n")
                f.write(f"BACKUP_DIR={backup_dir}\n")
            self.add_status_message("Tokens salvos no arquivo .env", "success")
        else:
            self.add_status_message("Configurações não salvas no arquivo .env pois a opção não foi marcada.", "info")

    def browse_directory(self):
        """Opens directory browser dialog"""
        directory = filedialog.askdirectory(
            title="Selecione o diretório de backup",
            initialdir="."
        )
        if directory:
            self.backup_section.backup_dir_entry.delete(0, tk.END)
            self.backup_section.backup_dir_entry.insert(0, directory)

    def refresh_repo_count(self):
        """Refreshes the repository count for the source account"""
        source_token = self.get_source_token()

        if not source_token:
            self.add_status_message("Erro: Token de origem é necessário", "error")
            self.token_section.set_repo_count_label("Repositórios: -")
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
                self.token_section.set_repo_count_label(f"Repositórios: {count}")
                self.add_status_message(f"Contagem atualizada: {count} repositórios encontrados", "success")
            except socket.error:
                raise Exception("Não foi possível conectar ao GitHub. Verifique sua conexão com a internet.")
        except Exception as e:
            error_msg = f"Erro ao obter contagem: {str(e)}"
            self.add_status_message(error_msg, "error")
            self.token_section.set_repo_count_label("Repositórios: -")

    # Placeholder commands for buttons - to be implemented later
    def start_backup(self):
        self.add_status_message("Backup iniciado...", "info")
        self.control_section.pause_button.config(state=tk.NORMAL)
        self.control_section.cancel_button.config(state=tk.NORMAL)
        self.control_section.start_button.config(state=tk.DISABLED)

    def pause_backup(self):
        self.add_status_message("Backup pausado.", "warning")
        self.control_section.pause_button.config(state=tk.DISABLED)
        self.control_section.start_button.config(state=tk.NORMAL)

    def cancel_backup(self):
        if messagebox.askyesno("Cancelar Backup", "Tem certeza que deseja cancelar o backup?"):
            self.add_status_message("Backup cancelado pelo usuário.", "error")
            self.control_section.pause_button.config(state=tk.DISABLED)
            self.control_section.cancel_button.config(state=tk.DISABLED)
            self.control_section.start_button.config(state=tk.NORMAL)
            self.update_progress(0)
