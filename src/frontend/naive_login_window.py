"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

class LoginWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 400)
        layout = QVBoxLayout()
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username"))
        username_layout.addWidget(QLineEdit())
        layout.addLayout(username_layout)
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password"))
        password_layout.addWidget(QLineEdit())
        layout.addLayout(password_layout)
        layout.addWidget(QPushButton("Login"))
        self.setLayout(layout)

class LoginWindow(LoginWindowUI):
    def __init__(self):
        super().__init__()
        
    def show(self):
        super().show()

if __name__ == "__main__":
    app = QApplication([])
    loginwindow = LoginWindow()
    loginwindow.show()
    
    exit(app.exec_())