import os

def validate_input():
    source_token = os.getenv('SOURCE_GITHUB_TOKEN', '').strip()
    dest_token = os.getenv('DEST_GITHUB_TOKEN', '').strip()
    backup_dir = os.getenv('BACKUP_DIR')

    if not source_token or not dest_token or not backup_dir:
        raise ValueError("Missing required environment variables")

    if not os.path.isdir(backup_dir):
        raise ValueError(f"Backup directory {backup_dir} does not exist or is not a directory")

    return source_token, dest_token, backup_dir
