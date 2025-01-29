import logging

import logging

class ErrorLogger:
    def __init__(self):
        self.logger = logging.getLogger('error_logger')
        self.logger.setLevel(logging.ERROR)
        handler = logging.FileHandler('error_log.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_error(self, exception, stage="General"):
        self.logger.error(f"Stage: {stage}, Exception: {exception}")

def setup_error_logger():
    return ErrorLogger()
