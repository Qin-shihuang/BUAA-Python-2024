"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Just a test file, NOT FOR PRODUCTION
"""

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget, QFormLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
# MARK: - UI
class LoginRegisterWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.center()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel#error_label {
                color: red;
                font-size: 12px;
            }
        """)

        
        layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        
        
        # MARK: Login Page
        login_widget = QWidget()
        login_layout = QVBoxLayout(login_widget)
        login_layout.addStretch(1)
        
        login_title = QLabel('Login')
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setFont(QFont('Arial', 20))
        login_layout.addWidget(login_title)
        
        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Username")
        login_layout.addWidget(self.login_username_input)
        
        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Password")
        self.login_password_input.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.login_password_input)
        
        self.login_error_label = QLabel()
        self.login_error_label.setObjectName("error_label")
        self.login_error_label.setStyleSheet("color: red")
        login_layout.addWidget(self.login_error_label)
        
        self.login_button = QPushButton("Login")
        login_layout.addWidget(self.login_button)
        
        switch_to_register_button = QPushButton("Don't have an account? Register")
        switch_to_register_button.setStyleSheet('background-color: transparent; color: #4CAF50;')
        switch_to_register_button.clicked.connect(self.switch_to_register)
        login_layout.addWidget(switch_to_register_button)
        
        login_layout.addStretch(1)
        
        # MARK: Register Page
        register_widget = QWidget()
        register_layout = QVBoxLayout(register_widget)
        register_layout.addStretch(1)
        
        register_title = QLabel('Register')
        register_title.setAlignment(Qt.AlignCenter)
        register_title.setFont(QFont('Arial', 20))
        register_layout.addWidget(register_title)
        
        self.register_username_input = QLineEdit()
        self.register_username_input.setPlaceholderText("Username")
        register_layout.addWidget(self.register_username_input)
        
        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Password")
        self.register_password_input.setEchoMode(QLineEdit.Password)
        
        register_layout.addWidget(self.register_password_input)
        
        self.register_password_repeat_input = QLineEdit()
        self.register_password_repeat_input.setPlaceholderText("Repeat Password")
        self.register_password_repeat_input.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_password_repeat_input)
        
        self.register_error_label = QLabel()
        self.register_error_label.setObjectName("error_label")
        self.register_error_label.setStyleSheet("color: red")
        register_layout.addWidget(self.register_error_label)
        
        self.register_button = QPushButton("Register")
        register_layout.addWidget(self.register_button)
        
        switch_to_login_button = QPushButton("Already have an account? Login")
        switch_to_login_button.setStyleSheet('background-color: transparent; color: #4CAF50;')
        switch_to_login_button.clicked.connect(self.switch_to_login)
        
        register_layout.addWidget(switch_to_login_button)
        
        register_layout.addStretch(1)
        
        self.stacked_widget.addWidget(login_widget)
        self.stacked_widget.addWidget(register_widget)
        
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
        
        # self.response_label = QLabel()
        # self.response_label.setStyleSheet("color: red")

        # form_layout = QFormLayout()
        # self.username_input = QLineEdit()
        # self.password_input = QLineEdit()
        # self.password_input.setEchoMode(QLineEdit.Password)


        # self.login_button = QPushButton("Login")
        # form_layout.addRow("Username", self.username_input)
        # form_layout.addRow("Password", self.password_input)
        # self.layout.addLayout(form_layout)
        # self.layout.addWidget(self.response_label)
        # self.layout.addWidget(self.login_button)
        # # TODO: register
        # self.setLayout(self.layout)
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def switch_to_register(self):
        self.stacked_widget.setCurrentIndex(1)
        
    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)

# MARK: - Logic
class LoginRegisterWindow(LoginRegisterWindowUI):
    # TODO: Login logic
    def __init__(self):
        super().__init__()
        self.login_button.clicked.connect(self.login_button_clicked)
        self.register_button.clicked.connect(self.register_button_clicked)
        
    def show(self):
        super().show()
    
    def login_button_clicked(self):
        self.login_error_label.setText(f"Logging in as {self.login_username_input.text()}...")
        
    def register_button_clicked(self):
        self.register_error_label.setText(f"Registering as {self.register_username_input.text()}...")



def try_login(username, password):
    # TODO: Connect to backend
    return True

# For debugging
if __name__ == "__main__":
    app = QApplication([])
    loginwindow = LoginRegisterWindow()
    loginwindow.show()
    exit(app.exec_())