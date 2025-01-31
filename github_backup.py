import os
import tkinter as tk
import sys
from dotenv import load_dotenv
from backup_logic import BackupExecutor
from backup_logic.progress_management import ProgressManager
from logger_config import setup_logger
from error_logger import setup_error_logger
from input_validation import validate_input
from backup_logic.token_validation import validate_token
from gui_components import BackupGUIComponents
from threading import Event, Thread

def run_cli():
    """Run the backup process in command line mode"""
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
            retry_count=3  # Default to 3 retries
        )

    except Exception as e:
        error_logger.log_error(e, "Error during backup")
        logger.error(f"Error during backup: {str(e)}")
        sys.exit(1)

def run_gui():
    """Run the backup process with GUI interface"""
    load_dotenv()

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
            source_token = gui.source_token_entry.get().strip()
            dest_token = gui.dest_token_entry.get().strip()
            backup_dir = gui.backup_dir_entry.get().strip()

            if not source_token or not dest_token or not backup_dir:
                gui.add_status_message("Erro: Todos os campos são obrigatórios", "error")
                return

            if not validate_token(source_token):
                gui.add_status_message("Erro: Token de origem inválido", "error")
                return
            if not validate_token(dest_token):
                gui.add_status_message("Erro: Token de destino inválido", "error")
                return

            # Save configuration if checkbox is checked
            if gui.save_config_var.get():
                with open('.env', 'w') as f:
                    f.write(f"SOURCE_GITHUB_TOKEN={source_token}\n")
                    f.write(f"DEST_GITHUB_TOKEN={dest_token}\n")
                    f.write(f"BACKUP_DIR={backup_dir}\n")

            # Disable start button and enable pause/cancel buttons
            gui.start_button.config(state=tk.DISABLED)
            gui.pause_button.config(state=tk.NORMAL)
            gui.cancel_button.config(state=tk.NORMAL)

            # Clear previous status
            gui.clear_status()
            gui.add_status_message("Iniciando processo de backup...", "info")

            def backup_thread():
                try:
                    backup_executor = BackupExecutor(logger, error_logger, progress_manager)
                    backup_executor.run_backup(
                        source_token=source_token,
                        dest_token=dest_token,
                        backup_dir=backup_dir,
                        progress_var=gui.progress_var,
                        is_running=True,
                        pause_event=pause_event,
                        cancel_event=cancel_event,
                        retry_count=int(gui.retry_count.get())
                    )

                    # Update GUI from main thread
                    root.after(0, lambda: gui.add_status_message("Backup concluído com sucesso!", "success"))
                    root.after(0, lambda: gui.show_success("Sucesso", "Backup concluído com sucesso!"))
                    root.after(0, lambda: complete_backup())

                except Exception as e:
                    error_msg = f"Erro durante o backup: {str(e)}"
                    error_logger.log_error(e, error_msg)
                    # Update GUI from main thread
                    root.after(0, lambda: gui.add_status_message(error_msg, "error"))
                    root.after(0, lambda: gui.show_error("Erro", error_msg))
                    root.after(0, lambda: complete_backup())

            def complete_backup():
                gui.start_button.config(state=tk.NORMAL)
                gui.pause_button.config(state=tk.DISABLED)
                gui.cancel_button.config(state=tk.DISABLED)
                pause_event.clear()  # Reset pause state

            # Start backup in separate thread
            backup_thread = Thread(target=backup_thread, daemon=True)
            backup_thread.start()

        except Exception as e:
            error_msg = f"Erro ao iniciar backup: {str(e)}"
            gui.add_status_message(error_msg, "error")
            error_logger.log_error(e, error_msg)
            gui.start_button.config(state=tk.NORMAL)
            gui.pause_button.config(state=tk.DISABLED)
            gui.cancel_button.config(state=tk.DISABLED)

    def cancel_backup():
        cancel_event.set()
        gui.add_status_message("Cancelando backup...", "warning")
        gui.cancel_button.config(state=tk.DISABLED)

    def toggle_pause():
        if pause_event.is_set():
            pause_event.clear()
            gui.pause_button.config(text="Pausar")
            gui.add_status_message("Retomando backup...", "info")
        else:
            pause_event.set()
            gui.pause_button.config(text="Retomar")
            gui.add_status_message("Pausando backup...", "warning")

    # Load values from .env if they exist
    gui.source_token_entry.insert(0, os.getenv('SOURCE_GITHUB_TOKEN', ''))
    gui.dest_token_entry.insert(0, os.getenv('DEST_GITHUB_TOKEN', ''))
    gui.backup_dir_entry.insert(0, os.getenv('BACKUP_DIR', ''))

    gui.start_button.config(command=start_backup)
    gui.pause_button.config(command=toggle_pause)
    gui.cancel_button.config(command=cancel_backup)  # Add cancel button handler

    root.mainloop()

if __name__ == "__main__":
    # Check if running in CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli()
    else:
        run_gui()
