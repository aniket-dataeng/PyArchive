import os
import gzip
import shutil
import humanize
import hashlib
from datetime import datetime
from scripts.database import DatabaseHandler
import json
import logging
import csv

class FileHandler:
    with open(os.path.expanduser("~/Projects/PyBak/config/config.json"), "r") as f:
        config = json.load(f)

    logging.basicConfig(
            filename=os.path.expanduser(config["log_file"]),   # Log file where logs will be saved
            level=logging.DEBUG,          # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp
        )
    
    def __init__(self, config):
        self.src_dir = os.path.expanduser(config["source_directory"])
        self.tgt_dir = os.path.expanduser(config["destination_directory"])
        self.timestamp_format = config["compression"]["timestamp_format"]
        self.db_handler = DatabaseHandler(config["database"])
        self.report_loc = os.path.expanduser(config["report"])
        ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.run_token = f"RUN_{ts}"
        
        # Ensure directories exist
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.tgt_dir, exist_ok=True)

    def compress_files(self):
        """Compress all files in the source directory and store them in the destination."""
        global run_token
        for file in os.listdir(self.src_dir):
            file_path = os.path.join(self.src_dir, file)

            if os.path.isfile(file_path):
                hexdigest = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()  
                logging.info(f"Processing: {file_path}")
                timestamp = datetime.now().strftime(self.timestamp_format)
                dup = self.db_handler.check_dups(hexdigest)
                #print(f"Dup Value: {dup}, {dup[0][0]}")
                if dup and dup[0] >= 1:
                    logging.info(f"Duplicate file so skipping archieval")
                    continue
                    
                
                compressed_filename = f"PyBak_{timestamp}_{file}.gz"
                compressed_path = os.path.join(self.tgt_dir, compressed_filename)
                orig_size = humanize.naturalsize(os.path.getsize(file_path))
                              
                # Compress the file
                with open(file_path, "rb") as f_in, gzip.open(compressed_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out, length=1024 * 1024)

                new_size = humanize.naturalsize(os.path.getsize(compressed_path))
                
                # Insert record into database
                self.db_handler.insert_file_record(file, compressed_filename, orig_size, new_size, hexdigest, self.run_token)

        logging.info("Compression completed.")
        self.gen_report()

    def get_backup_records(self):
        """Fetch and print all database records."""
        records = self.db_handler.get_all_records()
        for record in records:
            print(record)

    def gen_report(self):
        """Fetch and generate report for latest records."""
        logging.info("Generating Report")
        headers = ["Filename", "Compressed Filename", "Original Size (KB)", "Compressed Size (KB)", "Hex Digest"]
        records = self.db_handler.generate_report(self.run_token)
        csv_filename = os.path.join(self.report_loc,f"Report_{self.run_token}.csv")
        
        with open(csv_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(records)
        logging.info(f"Report generated {csv_filename}")






        