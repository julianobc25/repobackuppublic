import os
from dotenv import load_dotenv
from backup_logic import BackupExecutor
from backup_logic.progress_management import ProgressManager
from logger_config import setup_logger
from error_logger import setup_error_logger
from input_validation import validate_input
from backup_logic.token_validation import validate_token

def main():
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
        backup_executor.run_backup(source_token, dest_token, backup_dir, None, True, None)

    except Exception as e:
        error_logger.error(f"Error during backup: {str(e)}")
        logger.error(f"Error during backup: {str(e)}")

if __name__ == "__main__":
    main()
