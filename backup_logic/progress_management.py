import json
import os

class ProgressManager:
    def __init__(self, progress_file='progress.json'):
        self.progress_file = progress_file
        self.current_progress = self.load_progress()

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}

    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.current_progress, f, indent=4)
