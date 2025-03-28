import sqlite3
import os

class DatabaseHandler:
    def __init__(self, db_path, logger):
        self.db_path = os.path.expanduser(db_path)
        self.logger=logger
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self._create_table()
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            self.conn = None 
            
    def _create_table(self):
        if not self.conn:
            self.logger.error("Create table failed: No database connection.")
            return
            
        """Create the backup details table if it doesn't exist."""
        try:
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS PyBak_Details (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    FNAME TEXT,
                    COMPRESSED_FNAME TEXT,
                    ORIG_SIZE TEXT,
                    COMPRESSED_SIZE TEXT,
                    HEXDIGEST TEXT,
                    RUN_TOKEN TEXT
                );
                '''
            )
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Create table error: {e}")

    def insert_file_record(self, file,filename,orig_size,new_size,hexdigest,run_token):
        """Insert a new compressed file record into the database."""
        if not self.conn:
            self.logger.error("Insert failed: No database connection.")
            return
            
        try:
            self.cursor.execute("INSERT INTO PyBak_Details (FNAME, COMPRESSED_FNAME, ORIG_SIZE, COMPRESSED_SIZE,hexdigest, run_token) VALUES (?,?,?,?,?,?)", (file,filename,orig_size,new_size,hexdigest,run_token,))
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Insert error: {e}")
            
    def get_all_records(self):
        """Retrieve all records from the database."""
        if not self.conn:
            self.logger.error("Retrieve failed: No database connection.")
            return []
            
        try:
            self.cursor.execute("SELECT * FROM PyBak_Details")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Retrieve error: {e}")
            return []
            
    def check_dups(self, hexdigest):
        """Check for the duplicate hex digest value."""
        if not self.conn:
            self.logger.error("Duplicate check failed: No database connection.")
            return 1
            
        try:
            self.cursor.execute("SELECT count(1) FROM PyBak_Details where hexdigest = (?)", (hexdigest,))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            self.logger.error(f"Error while checking duplicates: {e}")
            return 1
            
    def generate_report(self, run_token):
        """Check for the duplicate hex digest value."""
        if not self.conn:
            self.logger.error("Generate Report failed: No database connection.")
            return []
            
        try:
            self.cursor.execute("SELECT FNAME, COMPRESSED_FNAME, ORIG_SIZE, COMPRESSED_SIZE,hexdigest FROM PyBak_Details where run_token = (?)", (run_token,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Error generating report: {e}")            

    def close(self):
        """Close the database connection."""
        if not self.conn:
            self.logger.error("Close failed: No database connection.")
            return
            
        try:
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error(f"Error closing connection: {e}") 
