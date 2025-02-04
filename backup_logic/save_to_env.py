import os
from tkinter import messagebox

class ConfigSaver:
    def __init__(self, gui_components, logger):
        self.gui_components = gui_components
        self.logger = logger

    def save_to_env(self):
        """Salva as configurações no arquivo .env"""
        if not self.gui_components.save_config_var.get():
            return

        env_content = f"""# Tokens do GitHub
SOURCE_GITHUB_TOKEN={self.gui_components.source_token_entry.get().strip()}
DEST_GITHUB_TOKEN={self.gui_components.dest_token_entry.get().strip()}
BACKUP_DIR={self.gui_components.backup_dir_entry.get().strip()}
"""
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            self.logger.info("Configurações salvas no arquivo .env")
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações no .env: {str(e)}")
            messagebox.showerror("Erro", f"Não foi possível salvar as configurações: {str(e)}")