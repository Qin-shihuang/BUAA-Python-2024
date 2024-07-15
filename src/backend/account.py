"""
Author: Iz0
Date: 2024-07-15
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

import bcrypt

import config
import backend.database as database

class IAccountManager:
    def register(self, username, password):
        pass
    
    def login(self, username, password):
        pass
    
class SimpleAccountManager(IAccountManager):
    def __init__(self):
        self.db = database.Database(config.account_db_name)
        self.db.create("account", ["username TEXT", "password TEXT"])
        
    def register(self, username, password):
        query = f"SELECT * FROM account WHERE username = '{username.lower()}'"
        if self.db.query(query):
            return False, "Username is already taken"
        hashed_password = bcrypt.hashpw(password.encode(), config.salt)
        query = f"INSERT INTO account (username, password) VALUES ('{username.lower()}', '{hashed_password.decode()}')"
        self.db.query(query)
        return True, ""
            
    def login(self, username, password):
        query = f"SELECT * FROM account WHERE username = '{username.lower()}'"
        user = self.db.query(query)
        if not user:
            return False, "Incorrect username or password"
        user = user[0]
        if bcrypt.checkpw(password.encode(), user[1].encode()):
            return True, ""
        return False, "Incorrect username or password"