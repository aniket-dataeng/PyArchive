import json
import os
from scripts.file_handler import FileHandler

# Load configuration
with open(os.path.expanduser("~/Projects/PyBak/config/config.json"), "r") as f:
    config = json.load(f)

# Initialize FileHandler
file_handler = FileHandler(config)

# Run compression process
file_handler.compress_files()

# Print backup records
#file_handler.get_backup_records()
