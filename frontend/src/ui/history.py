import os
import sys
from PyQt5.QtCore import Qt, QDateTime, QFileInfo, pyqtSignal, QRect, QSize, QPoint
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox, QMenu, QAction, QMessageBox


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("History")
        self.resize(900, 600)
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
            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: #e0e0e0;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                height: 0;
                width: 0;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-page:vertical,
            QScrollBar::add-page:vertical {
                background: none;
                width: 0px;
                height: 0px;
            }
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # MARK: User Info
        logout_layout = QHBoxLayout()
        logout_layout.addStretch(1)

        self.user_info_label = QLabel()
        username = self.get_username()
        self.user_info_label.setText(f"Welcome, {username} ")
        self.user_info_label.setFont(QFont('Arial', 13))
        logout_layout.addWidget(self.user_info_label)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.switch_to_login_window)
        logout_layout.addWidget(self.logout_button)
        layout.addLayout(logout_layout)

        self.history_widget = QWidget()
        history_title_label = QLabel('<p style="color: green">历史查重任务</p>')
        history_title_label.setFont(QFont('Arial', 20, QFont.Bold))

        history_layout = QVBoxLayout()
        history_layout.addWidget(history_title_label)
        self.history_widget.setLayout(history_layout)

        return_button = QPushButton('return')
        history_layout.addWidget(return_button)

        layout.addWidget(self.history_widget)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def get_username(self):
        return "admin"
        # TODO: Get username from login window

    def switch_to_login_window(self):
        # self.login_window = LoginWindow(self.switch_to_login_window)
        # self.login_window.show()
        self.close()


if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    history_page = HistoryPage()
    history_page.show()
    exit(app.exec_())
