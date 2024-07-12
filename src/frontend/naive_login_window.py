"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout

class LoginWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.layout = QVBoxLayout()
        
        self.response_label = QLabel()
        
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()

        self.login_button = QPushButton("Login")
        form_layout.addRow("Username", self.username_input)
        form_layout.addRow("Password", self.password_input)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.response_label)
        self.layout.addWidget(self.login_button)
        # TODO: register
        self.setLayout(self.layout)

class LoginWindow(LoginWindowUI):
    # TODO: Login logic
    def __init__(self):
        super().__init__()
        self.login_button.clicked.connect(self.login_button_clicked)
        
    def show(self):
        super().show()
    
    def login_button_clicked(self):
        self.response_label.setStyleSheet("color: red")
        self.response_label.setText("Login button clicked!")

if __name__ == "__main__":
    app = QApplication([])
    loginwindow = LoginWindow()
    loginwindow.show()
    
    exit(app.exec_())