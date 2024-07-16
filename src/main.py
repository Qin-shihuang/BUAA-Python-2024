"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Entry point of the application
"""

import os
import sys

import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from backend.account import SimpleAccountManager
from frontend.login_register_window import LoginRegisterWindow
from frontend.main_window import MainWindowUI

if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    app = QApplication(sys.argv)
    account_manager = SimpleAccountManager()
    main_window = MainWindowUI()
    login_register_window = LoginRegisterWindow(account_manager, main_window.show)
    login_register_window.show()
    
    exit(app.exec_())
