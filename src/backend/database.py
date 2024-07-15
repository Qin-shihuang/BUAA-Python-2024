"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

import sqlite3

class Database:
    def __init__(self, db_name):
        db_path = f"data/{db_name}.db"
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        if not self.conn:
            raise Exception("Failed to connect to the database")

    def __del__(self):
        self.conn.close()
    
    def close(self):
        self.conn.close()
        
    def create(self, table_name, columns):
        # check if the table already exists
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        if self.query(query):
            return
        columns = ", ".join(columns)
        self.cursor.execute(f"CREATE TABLE {table_name} ({columns})")
        self.conn.commit()
        
    def query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()
    