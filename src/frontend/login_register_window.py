"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Login window module
"""

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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
        
        self.password_requirements_label = QLabel()
        self.password_requirements_label.setAlignment(Qt.AlignLeft)
        register_layout.addWidget(self.password_requirements_label)
        
        self.register_error_label = QLabel()
        self.register_error_label.setObjectName("error_label")
        self.register_error_label.setStyleSheet("color: red")
        self.password_requirements_label.setContentsMargins(10, 0, 0, 0)
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
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def switch_to_register(self):
        self.register_error_label.setText("")
        self.register_username_input.setText("")
        self.register_password_input.setText("")
        self.register_password_repeat_input.setText("")
        self.stacked_widget.setCurrentIndex(1)
        
    def switch_to_login(self):
        self.login_error_label.setText("")
        self.login_username_input.setText("")
        self.login_password_input.setText("")
        self.stacked_widget.setCurrentIndex(0)

# MARK: - Logic
class LoginRegisterWindow(LoginRegisterWindowUI):
    def __init__(self, accountManager=None, loginCallback=None):
        super().__init__()
        self.account_manager = accountManager
        self.login_callback = loginCallback
        self.login_button.clicked.connect(self.login_button_clicked)
        self.register_button.clicked.connect(self.register_button_clicked)
        self.register_password_input.textChanged.connect(self.update_password_requirements)
        self.register_password_repeat_input.focusOutEvent = self.register_password_repeat_lost_focus
    
    def login_button_clicked(self):
        error_text = ""
        if self.login_username_input.text() == "":
            error_text = "Username cannot be empty."
        elif self.login_password_input.text() == "":
            error_text = "Password cannot be empty."
        else:
            if self.account_manager:
                success, message = self.account_manager.login(self.login_username_input.text(), self.login_password_input.text())
                if success:
                    if self.login_callback:
                        self.login_callback()
                        self.close()
                    return
                else:
                    error_text = message
            else:
                error_text = "AccountManager not registered!"
        self.login_error_label.setStyleSheet("color: red")
        self.login_error_label.setText(error_text)

            
        
    def register_button_clicked(self):  
        error_text = ""
        if self.register_username_input == "":
            error_text = "Username cannot be empty."
        elif not self.register_username_input.text().isalnum():
            error_text = "Username can only contain letters and numbers."
        elif self.register_password_input == "":
            error_text = "Password cannot be empty."
        elif not check_password_validity(self.register_password_input.text()):
            error_text = "Password does not satisfy requirements."
        elif self.register_password_input.text() != self.register_password_repeat_input.text():
            error_text = "Passwords do not match."
        else:
            if self.account_manager:
                success, message = self.account_manager.register(self.register_username_input.text(), self.register_password_input.text())
                if success:
                    self.stacked_widget.setCurrentIndex(0)
                    self.login_error_label.setStyleSheet("color: green")
                    self.login_error_label.setText(f"Registered successfully! Please login.")
                    self.login_username_input.setText(self.register_username_input.text())
                else:
                    error_text = message
            else:
                error_text = "AccountManager not registered!"
        self.register_error_label.setStyleSheet("color: red")
        self.register_error_label.setText(error_text)

    def register_password_repeat_lost_focus(self, event):
        if self.register_password_input.text() != self.register_password_repeat_input.text():
            self.register_error_label.setText("Passwords do not match")
        else:
            self.register_error_label.setText("")
        QLineEdit.focusOutEvent(self.register_password_repeat_input, event)

    def update_password_requirements(self):
        pw = self.register_password_input.text()
        requirements = [
            (len(pw) >= 8, "At least 8 characters"),
            (any(char.isdigit() for char in pw), "At least one number"),
            (any(char.isupper() for char in pw), "At least one uppercase letter"),
            (any(char.islower() for char in pw), "At least one lowercase letter"),
            (all(char.isalnum() or char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in pw), "Only letters, numbers and special characters")
        ]
        style = "<p style='line-height: 1.0; margin: 0 0 5px 0'>Password requirements:</p>"

        for status, req in requirements:
            color = "green" if status else "red"
            indicator = "✓" if status else "✗"

            style += f'<p style="color:{color}; line-height: 1.0; margin: 0 0 2px 0">{indicator} {req}</p>'

        self.password_requirements_label.setText(style)

def check_password_validity(password):
    if len(password) < 8:
        return False 
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not all(char.isalnum() or char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password):
        return False
    return True
    
# For debugging
if __name__ == "__main__":
    app = QApplication([])
    loginwindow = LoginRegisterWindow()
    loginwindow.show()
    exit(app.exec_())