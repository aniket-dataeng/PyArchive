import logging
import os

class LogHandler:
    def __init__(self, config):
        self.lvl = config["log_level"]
        self.fname = os.path.join(os.path.expanduser(config["log_file"]))
        logging.basicConfig(
            filename=self.fname,   # Log file where logs will be saved
            level=self.lvl,          # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp
        )