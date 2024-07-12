"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class LoginWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Username"))
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QLabel("Password"))
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QPushButton("Login"))
        self.setLayout(self.layout)

class LoginWindow(LoginWindowUI):
    def __init__(self):
        super().__init__()
        
    def show(self):
        super().show()
