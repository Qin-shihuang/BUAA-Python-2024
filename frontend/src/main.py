"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: Entry point of the application
"""

import sys

import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui.login import LoginWindow
from ui.file_picker import FileUploadWidget
from ui.login_history import LoginHistoryWidget

if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    app = QApplication(sys.argv)
    file_upload_widget = FileUploadWidget()        
    login_history_widget = LoginHistoryWidget()
    
    login_window = LoginWindow(login_history_widget.show)
    login_window.show()
    
    exit(app.exec_())
