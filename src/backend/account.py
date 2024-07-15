"""
Author: Iz0
Date: 2024-07-15
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

import bcrypt

import config
import backend.database as database

# account database:
# username, password(hashed)

class AccountManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self):
        self.db = database.Database(config.account_db_name)
        self.db.create("account", ["username TEXT", "password TEXT"])
        
    # returns (bool, str)
    def register(self, username, password):
        # check if the username is already taken
        query = f"SELECT * FROM account WHERE username = '{username}'"
        if self.db.query(query):
            return False, "Username is already taken"
        hashed_password = bcrypt.hashpw(password.encode(), config.salt)
        query = f"INSERT INTO account (username, password) VALUES ('{username}', '{hashed_password.decode()}')"
        self.db.query(query)
        return True, ""
            
    def login(self, username, password):
        query = f"SELECT * FROM account WHERE username = '{username}'"
        user = self.db.query(query)
        if not user:
            return False, "Incorrect username or password"
        user = user[0]
        if bcrypt.checkpw(password.encode(), user[1].encode()):
            return True, ""
        return False, "Incorrect username or password"