import json
import os
import threading
import time
from pathlib import Path
from typing import Dict, Optional
from threading import Lock, Event

class ProgressState:
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

class ProgressManager:
    def __init__(self, progress_file='progress.json'):
        self.progress_file = Path(progress_file)
        self.backup_file = self.progress_file.with_suffix('.json.bak')
        self.lock = Lock()
        self.pause_event = Event()
        self.current_progress: Dict = {}
        self.state = ProgressState.RUNNING
        self._load_progress()

    def _atomic_write(self, file_path: Path, data: Dict) -> None:
        """Write data to file atomically to prevent corruption."""
        temp_file = file_path.with_suffix('.tmp')
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=4)
            temp_file.replace(file_path)
        except Exception:
            if temp_file.exists():
                temp_file.unlink()
            raise

    def _load_progress(self) -> None:
        """Load progress from file with backup recovery."""
        try:
            if self.progress_file.exists():
                with open(self.progress_file, 'r') as f:
                    self.current_progress = json.load(f)
            elif self.backup_file.exists():
                with open(self.backup_file, 'r') as f:
                    self.current_progress = json.load(f)
                    # Restore from backup
                    self._atomic_write(self.progress_file, self.current_progress)
        except json.JSONDecodeError:
            # If main file is corrupt, try backup
            if self.backup_file.exists():
                with open(self.backup_file, 'r') as f:
                    self.current_progress = json.load(f)
            else:
                self.current_progress = {}
        except Exception:
            self.current_progress = {}

    def save_progress(self) -> None:
        """Save progress to file with thread safety and backup."""
        with self.lock:
            try:
                # First backup existing file if it exists
                if self.progress_file.exists():
                    self._atomic_write(self.backup_file, self.current_progress)
                
                # Then write new progress
                self._atomic_write(self.progress_file, self.current_progress)
            except Exception as e:
                raise Exception(f"Erro ao salvar progresso: {str(e)}")

    def update_progress(self, repo_name: str, status: str) -> None:
        """Update progress for a repository with thread safety."""
        with self.lock:
            self.current_progress[repo_name] = {
                'status': status,
                'timestamp': time.time()
            }
            self.save_progress()

    def get_progress(self, repo_name: str) -> Optional[Dict]:
        """Get progress for a repository with thread safety."""
        with self.lock:
            return self.current_progress.get(repo_name)

    def clear_progress(self) -> None:
        """Clear all progress with thread safety."""
        with self.lock:
            self.current_progress = {}
            self.save_progress()

    def set_state(self, state: str) -> None:
        """Set the current state with thread safety."""
        with self.lock:
            self.state = state
            if state == ProgressState.PAUSED:
                self.pause_event.set()
            else:
                self.pause_event.clear()
            self.current_progress['_state'] = state
            self.save_progress()

    def get_state(self) -> str:
        """Get the current state with thread safety."""
        with self.lock:
            return self.state

    def is_paused(self) -> bool:
        """Check if the backup is paused."""
        return self.pause_event.is_set()

    def wait_if_paused(self) -> None:
        """Wait if the backup is paused."""
        self.pause_event.wait()

    def get_incomplete_repos(self) -> Dict[str, Dict]:
        """Get repositories that haven't completed backup."""
        with self.lock:
            return {
                name: info
                for name, info in self.current_progress.items()
                if name != '_state' and info.get('status') != 'completed'
            }

    def get_failed_repos(self) -> Dict[str, Dict]:
        """Get repositories that failed backup."""
        with self.lock:
            return {
                name: info
                for name, info in self.current_progress.items()
                if name != '_state' and info.get('status') == 'error'
            }

    def can_resume(self) -> bool:
        """Check if there are repositories that can be resumed."""
        with self.lock:
            return bool(self.get_incomplete_repos())

    def cleanup_old_progress(self, max_age_days: int = 7) -> None:
        """Remove progress entries older than specified days."""
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        with self.lock:
            self.current_progress = {
                name: info
                for name, info in self.current_progress.items()
                if name == '_state' or
                (current_time - info.get('timestamp', 0)) < max_age_seconds
            }
            self.save_progress()
