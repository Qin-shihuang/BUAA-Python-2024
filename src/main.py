"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Entry point of the application
"""

from PyQt5.QtWidgets import QApplication

from backend.account import SimpleAccountManager
from frontend.login_register_window import LoginRegisterWindow
from frontend.main_window import MainWindowUI

if __name__ == "__main__":
    app = QApplication([])
    account_manager = SimpleAccountManager()
    main_window = MainWindowUI()
    login_register_window = LoginRegisterWindow(account_manager, main_window.show)
    login_register_window.show()
    
    exit(app.exec_())
