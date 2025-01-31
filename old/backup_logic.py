from backup_logic.token_validation import TokenValidator
from backup_logic.disk_space_check import DiskSpaceChecker
from backup_logic.save_to_env import EnvSaver
from backup_logic.progress_management import ProgressManager
from backup_logic.backup_execution import BackupExecutor

class BackupLogic:
    def __init__(self, gui_components, logger, error_logger):
        self.gui_components = gui_components
        self.logger = logger
        self.error_logger = error_logger
        self.token_validator = TokenValidator(gui_components, logger, error_logger)
        self.disk_space_checker = DiskSpaceChecker(error_logger)
        self.env_saver = EnvSaver(gui_components, logger)
        self.progress_manager = ProgressManager(logger)
        self.backup_executor = BackupExecutor(logger, error_logger, self.progress_manager)

    def validate_tokens(self):
        return self.token_validator.validate_tokens()

    def check_disk_space(self, path: str) -> bool:
        return self.disk_space_checker.check_disk_space(path)

    def save_to_env(self):
        self.env_saver.save_to_env()

    def load_progress(self):
        self.progress_manager.load_progress()

    def save_progress(self):
        self.progress_manager.save_progress()

    def run_backup(self, source_token, dest_token, backup_dir, progress_var, is_running, pause_event):
        self.backup_executor.run_backup(source_token, dest_token, backup_dir, progress_var, is_running, pause_event)