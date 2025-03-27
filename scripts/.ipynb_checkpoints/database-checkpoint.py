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
                HEXDIGEST TEXT
            );
            '''
        )
        self.conn.commit()

    def insert_file_record(self, file,filename,orig_size,new_size,hexdigest):
        """Insert a new compressed file record into the database."""
        self.cursor.execute("INSERT INTO PyBak_Details (FNAME, COMPRESSED_FNAME, ORIG_SIZE, COMPRESSED_SIZE,hexdigest) VALUES (?,?,?,?,?)", (file,filename,orig_size,new_size,hexdigest,))
        self.conn.commit()

    def get_all_records(self):
        """Retrieve all records from the database."""
        self.cursor.execute("SELECT * FROM PyBak_Details")
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
