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
    def __init__(self, config):
        try:
            logging.basicConfig(
                filename=os.path.expanduser(config["log_file"]),   # Log file where logs will be saved
                level=logging.DEBUG,          # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp
            )
        
            logger = logging.getLogger(__name__)
            self.src_dir = os.path.expanduser(config["source_directory"])
            self.tgt_dir = os.path.expanduser(config["destination_directory"])
            self.timestamp_format = config["compression"]["timestamp_format"]
            self.db_handler = DatabaseHandler(config["database"], logger=logger)
            self.report_loc = os.path.expanduser(config["report"])
            ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            self.run_token = f"RUN_{ts}"
            
            # Ensure directories exist
            os.makedirs(self.src_dir, exist_ok=True)
            os.makedirs(self.tgt_dir, exist_ok=True)
            os.makedirs(self.report_loc, exist_ok=True)
            
        except Exception as e:
            logging.error(f"Error initializing FileHandler: {e}")
            raise

    def compress_files(self):
        """Compress all files in the source directory and store them in the destination."""
        for file in os.listdir(self.src_dir):
            file_path = os.path.join(self.src_dir, file)

            if os.path.isfile(file_path):
                try:
                    hexdigest = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()  
                except Exception as e:
                    logging.error(f"Error calculating hexdigest for: {file_path} & {e}")
                    break
                    
                logging.info(f"Processing: {file_path}")
                timestamp = datetime.now().strftime(self.timestamp_format)

                try:
                    dup = self.db_handler.check_dups(hexdigest)                
                    if dup and dup >= 1:
                        logging.info(f"Duplicate file so skipping archieval")
                        continue
                except Exception as e:
                    logging.error(f"Error checking duplicate for: {file_path} & {e}")
                    break                    
                    
                
                compressed_filename = f"PyBak_{timestamp}_{file}.gz"
                compressed_path = os.path.join(self.tgt_dir, compressed_filename)
                orig_size = humanize.naturalsize(os.path.getsize(file_path))
                              
                # Compress the file
                try:
                    with open(file_path, "rb") as f_in, gzip.open(compressed_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out, length=1024 * 1024)
                except Exception as e:
                    logging.error(f"Error compressing the file: {e}")
                    raise
                    
                new_size = humanize.naturalsize(os.path.getsize(compressed_path))
                
                # Insert record into database
                try:
                    self.db_handler.insert_file_record(file, compressed_filename, orig_size, new_size, hexdigest, self.run_token)
                except Exception as e:
                    logging.error(f"Error while inserting records to table: {e}")
                    raise
                    
        logging.info("Compression completed.")
        self.gen_report()

    def get_backup_records(self):
        """Fetch and print all database records."""
        try: 
            records = self.db_handler.get_all_records()
            for record in records:
                print(record)
        except Exception as e:
            logging.error(f"Error while generating report - FH: {e}")
            raise

    def gen_report(self):
        """Fetch and generate report for latest records."""
        logging.info("Generating Report")
        headers = ["Filename", "Compressed Filename", "Original Size (KB)", "Compressed Size (KB)", "Hex Digest"]
        try:
            records = self.db_handler.generate_report(self.run_token)
            csv_filename = os.path.join(self.report_loc,f"Report_{self.run_token}.csv")
        
            with open(csv_filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(records)
            logging.info(f"Report generated {csv_filename}")
        
        except Exception as e:
            logging.error(f"Error while generating report - FH: {e}")
            raise         
        
     