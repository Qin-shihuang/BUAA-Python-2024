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

from ui.login import LoginWindow

if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    app = QApplication(sys.argv)
    login_window = LoginWindow(None)
    login_window.show()
    
    exit(app.exec_())
