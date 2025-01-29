import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.') / '.env'
load_dotenv(dotenv_path=dotenv_path)

source_token = os.getenv('SOURCE_GITHUB_TOKEN')
dest_token = os.getenv('DEST_GITHUB_TOKEN')
backup_dir = os.getenv('BACKUP_DIR')

print(f"SOURCE_GITHUB_TOKEN: {source_token}")
print(f"DEST_GITHUB_TOKEN: {dest_token}")
print(f"BACKUP_DIR: {backup_dir}")