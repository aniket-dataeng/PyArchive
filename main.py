import json
import os

with open(os.path.expanduser("~/Projects/PyBak/config/config.json"), "r") as f:
    config = json.load(f)

src_dir = os.path.expanduser(config["source_directory"])
dest_dir = os.path.expanduser(config["destination_directory"])
log_file = os.path.expanduser(config["log_file"])
zip_format = config["compression"]["format"]
ts_format = config["compression"]["timestamp_format"]
email_dict = config["email"]

print(email_dict)