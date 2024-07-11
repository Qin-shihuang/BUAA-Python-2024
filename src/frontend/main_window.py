"""
Author: Iz0
Date: 2024-07-12
License: MIT License
Description: 
"""


from PyQt5.QtWidgets import QApplication, QWidget

def main():
    app = QApplication([])
    window = QWidget()
    window.show()
    app.exec_()