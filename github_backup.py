import os
import tkinter as tk
import sys
import os
from dotenv import load_dotenv, find_dotenv
from backup_logic.backup_execution import BackupExecutor
from backup_logic import backup_execution
from backup_logic.progress_management import ProgressManager
from logger_config import setup_logger
from error_logger import setup_error_logger
from input_validation import validate_input
from backup_logic.token_validation import validate_token
from gui.gui_components import BackupGUIComponents
from threading import Event, Thread

def run_cli():
    """Run the backup process in command line mode"""
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
    load_dotenv()

    logger = setup_logger()
    error_logger = setup_error_logger()
    progress_manager = ProgressManager()

    try:
        source_token, dest_token, backup_dir = validate_input()

        if not validate_token(source_token):
            raise ValueError("Invalid source GitHub token")
        if not validate_token(dest_token):
            raise ValueError("Invalid destination GitHub token")

        backup_executor = BackupExecutor(logger, error_logger, progress_manager)
        backup_executor.run_backup(
            source_token=source_token,
            dest_token=dest_token,
            backup_dir=backup_dir,
            progress_var=None,
            is_running=True,
            pause_event=None,
            cancel_event=None,
            retry_count=2  # Default to 2 retries
        )

    except Exception as e:
        error_logger.log_error(e, "Error during backup")
        logger.error(f"Error during backup: {str(e)}")
        sys.exit(1)

def run_gui():
    """Run the backup process with GUI interface"""
    # Reload environment variables without clearing existing ones
    find_dotenv()
    load_dotenv(override=True)

    root = tk.Tk()
    root.title("GitHub Repository Backup Tool")
    
    logger = setup_logger()
    error_logger = setup_error_logger()
    progress_manager = ProgressManager()
    
    gui = BackupGUIComponents(root, logger, error_logger)
    pause_event = Event()
    cancel_event = Event()

    def start_backup():
        try:
            source_token = gui.token_section.get_source_token()
            dest_token = gui.token_section.get_dest_token()
            backup_dir = gui.backup_section.get_backup_dir()

            if not source_token or not dest_token or not backup_dir:
                gui.status_section.add_status_message("Erro: Todos os campos são obrigatórios", "error")
                return

            if not validate_token(source_token):
                gui.status_section.add_status_message("Erro: Token de origem inválido", "error")
                return
            if not validate_token(dest_token):
                gui.status_section.add_status_message("Erro: Token de destino inválido", "error")
                return

            # Save configuration if checkbox is checked
            if gui.options_section.get_save_config_var():
                with open('.env', 'w') as f:
                    f.write(f"SOURCE_GITHUB_TOKEN={source_token}\n")
                    f.write(f"DEST_GITHUB_TOKEN={dest_token}\n")
                    f.write(f"BACKUP_DIR={backup_dir}\n")

            # Disable start button and enable pause/cancel buttons
            gui.control_section.start_button.config(state=tk.DISABLED)
            gui.control_section.pause_button.config(state=tk.NORMAL)
            gui.control_section.cancel_button.config(state=tk.NORMAL)

            # Clear previous status
            gui.status_section.clear_status()
            gui.status_section.add_status_message("Iniciando processo de backup...", "info")

            def backup_thread():
                try:
                    backup_executor = BackupExecutor(logger, error_logger, progress_manager)
                    backup_executor.run_backup(
                        source_token=source_token,
                        dest_token=dest_token,
                        backup_dir=backup_dir,
                        progress_var=gui.status_section.progress_var,
                        is_running=True,
                        pause_event=pause_event,
                        cancel_event=cancel_event,
                        retry_count=gui.options_section.get_retry_count(),
                        repo_limit=gui.options_section.get_repo_limit() # Pass repo limit
                    )

                    # Update GUI from main thread
                    root.after(0, lambda: gui.status_section.add_status_message("Backup concluído com sucesso!", "success"))
                    root.after(0, lambda: gui.show_success("Sucesso", "Backup concluído com sucesso!"))
                    root.after(0, lambda: complete_backup())

                except Exception as e:
                    error_msg = f"Erro durante o backup: {str(e)}"
                    error_logger.log_error(e, error_msg)
                    # Update GUI from main thread
                    root.after(0, lambda: gui.status_section.add_status_message(error_msg, "error"))
                    root.after(0, lambda: gui.show_error("Erro", error_msg))
                    root.after(0, lambda: complete_backup())

            def complete_backup():
                gui.control_section.start_button.config(state=tk.NORMAL)
                gui.control_section.pause_button.config(state=tk.DISABLED)
                gui.control_section.cancel_button.config(state=tk.DISABLED)
                pause_event.clear()  # Reset pause state

            # Start backup in separate thread
            backup_thread = Thread(target=backup_thread, daemon=True)
            backup_thread.start()

        except Exception as e:
            error_msg = f"Erro ao iniciar backup: {str(e)}"
            gui.status_section.add_status_message(error_msg, "error")
            error_logger.log_error(e, error_msg)
            gui.control_section.start_button.config(state=tk.NORMAL)
            gui.control_section.pause_button.config(state=tk.DISABLED)
            gui.control_section.cancel_button.config(state=tk.DISABLED)

    def cancel_backup():
        cancel_event.set()
        gui.add_status_message("Cancelando backup...", "warning")
        gui.control_section.cancel_button.config(state=tk.DISABLED)

    def toggle_pause():
        if pause_event.is_set():
            pause_event.clear()
            gui.control_section.pause_button.config(text="Pausar")
            gui.add_status_message("Retomando backup...", "info")
        else:
            pause_event.set()
            gui.control_section.pause_button.config(text="Retomar")
            gui.add_status_message("Pausando backup...", "warning")

    # Load values from .env if they exist
    gui.token_section.source_token_entry.insert(0, os.getenv('SOURCE_GITHUB_TOKEN', ''))
    gui.token_section.dest_token_entry.insert(0, os.getenv('DEST_GITHUB_TOKEN', ''))
    gui.backup_section.backup_dir_entry.insert(0, os.getenv('BACKUP_DIR', ''))

    gui.control_section.start_button.config(command=start_backup)
    gui.control_section.pause_button.config(command=toggle_pause)
    gui.control_section.cancel_button.config(command=cancel_backup)  # Add cancel button handler

    root.mainloop()

if __name__ == "__main__":
    # Check if running in CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli()
    else:
        run_gui()
