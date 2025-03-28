import sqlite3
import os

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = os.path.expanduser(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the backup details table if it doesn't exist."""
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

    def insert_file_record(self, file,filename,orig_size,new_size,hexdigest,run_token):
        """Insert a new compressed file record into the database."""
        self.cursor.execute("INSERT INTO PyBak_Details (FNAME, COMPRESSED_FNAME, ORIG_SIZE, COMPRESSED_SIZE,hexdigest, run_token) VALUES (?,?,?,?,?,?)", (file,filename,orig_size,new_size,hexdigest,run_token,))
        self.conn.commit()

    def get_all_records(self):
        """Retrieve all records from the database."""
        self.cursor.execute("SELECT * FROM PyBak_Details")
        return self.cursor.fetchall()

    def check_dups(self, hexdigest):
        """Check for the duplicate hex digest value."""
        self.cursor.execute("SELECT count(1) FROM PyBak_Details where hexdigest = (?)", (hexdigest,))
        return self.cursor.fetchone()

    def generate_report(self, run_token):
        """Check for the duplicate hex digest value."""
        self.cursor.execute("SELECT FNAME, COMPRESSED_FNAME, ORIG_SIZE, COMPRESSED_SIZE,hexdigest FROM PyBak_Details where run_token = (?)", (run_token,))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
