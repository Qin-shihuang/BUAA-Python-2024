"""
Author: Iz0
Date: 2024-07-16
License: MIT License
Description: Login controller
"""

from PyQt5.QtCore import QObject

from utils.error_codes import ErrorCode
from utils.api_client import ApiClient

class LoginController(QObject):
    def __init__(self):
        self.api_client = ApiClient()
        
    def try_login(self, username, password):
        if username == "":
            return ErrorCode.USERNAME_EMPTY
        if password == "":
            return ErrorCode.PASSWORD_EMPTY
        return self.api_client.login(username, password)
    
    def try_register(self, username, password, confirmPassword) -> ErrorCode:
        if username == "":
            return ErrorCode.USERNAME_EMPTY
        if len(username) > 20:
            return ErrorCode.USERNAME_TOO_LONG
        if password == "":
            return ErrorCode.PASSWORD_EMPTY
        if any(not requirement for requirement, _ in self.check_password_requirements(password)):
            return ErrorCode.PASSWORD_INVALID
        if password != confirmPassword:
            return ErrorCode.PASSWORDS_MISMATCH
        return self.api_client.register(username, password)
        
    def check_password_requirements(self, password):
        return [
            (len(password) >= 8, "At least 8 characters"),
            (any(char.isdigit() for char in password), "At least one number"),
            (any(char.isupper() for char in password), "At least one uppercase letter"),
            (any(char.islower() for char in password), "At least one lowercase letter"),
            (all(char.isalnum() or char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password), "Only letters, numbers and special characters")
        ]
            
        
