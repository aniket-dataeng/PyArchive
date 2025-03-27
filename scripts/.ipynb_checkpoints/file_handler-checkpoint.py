import os
import gzip
import shutil
import humanize
import hashlib
from datetime import datetime
from scripts.database import DatabaseHandler

class FileHandler:
    def __init__(self, config):
        self.src_dir = os.path.expanduser(config["source_directory"])
        self.tgt_dir = os.path.expanduser(config["destination_directory"])
        self.timestamp_format = config["compression"]["timestamp_format"]
        self.db_handler = DatabaseHandler(config["database"])

        # Ensure directories exist
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.tgt_dir, exist_ok=True)

    def compress_files(self):
        """Compress all files in the source directory and store them in the destination."""
        for file in os.listdir(self.src_dir):
            file_path = os.path.join(self.src_dir, file)

            if os.path.isfile(file_path):
                hexdigest = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()  
                print(f"Processing: {file_path}")

                dup = self.db_handler.check_dups(hexdigest)
                #print(f"Dup Value: {dup}, {dup[0][0]}")
                if dup and dup[0][0] >= 1:
                    print(f"Duplicate file: {dup} --> {file_path}")
                    continue
                    
                timestamp = datetime.now().strftime(self.timestamp_format)
                compressed_filename = f"PyBak_{timestamp}_{file}.gz"
                compressed_path = os.path.join(self.tgt_dir, compressed_filename)
                orig_size = humanize.naturalsize(os.path.getsize(file_path))
                              
                # Compress the file
                with open(file_path, "rb") as f_in, gzip.open(compressed_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out, length=1024 * 1024)

                new_size = humanize.naturalsize(os.path.getsize(compressed_path))
                
                # Insert record into database
                self.db_handler.insert_file_record(file, compressed_filename, orig_size, new_size, hexdigest)

        print("Compression completed.")

    def get_backup_records(self):
        """Fetch and print all database records."""
        records = self.db_handler.get_all_records()
        for record in records:
            print(record)
