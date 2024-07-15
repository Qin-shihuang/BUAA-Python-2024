"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Entry point of the application
"""

from PyQt5.QtWidgets import QApplication

from frontend.login_register_window import LoginRegisterWindow

if __name__ == "__main__":
    app = QApplication([])
    loginwindow = LoginRegisterWindow()
    loginwindow.show()
    
    exit(app.exec_())
