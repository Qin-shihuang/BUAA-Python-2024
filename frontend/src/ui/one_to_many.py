import os
import sys
from PyQt5.QtCore import Qt, QDateTime, QFileInfo, pyqtSignal, QRect, QSize, QPoint
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor, QColor
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox, QMenu, QAction, QMessageBox


class OneToManyPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome")
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
            QTableWidget {
               border-radius: 5px;
               font-size: 13px;
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

        self.check_widget = QWidget()
        layout.addWidget(self.check_widget)

        title_label = QLabel('<p style="color: green">一对多查重</p>')
        title_label.setFont(QFont('Arial', 20, QFont.Bold))

        self.target_file_label = QLabel('目标文件')
        self.target_file_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.target_file_input = QLineEdit()
        self.target_file_input.setReadOnly(True)
        self.target_file_input.setFont(QFont('Arial', 10, QFont.Bold))
        self.target_file_input.setText(self.get_target_file())

        target_file_layout = QHBoxLayout()
        target_file_layout.addWidget(self.target_file_label)
        target_file_layout.addWidget(self.target_file_input)

        self.file_table = QTableWidget()
        # TODO: init file table items from backend
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.file_table.setColumnWidth(0, 60)

        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(('名称', '大小', '上传时间', '路径', '相似度'))

        header_item = QTableWidgetItem('相似度')
        header_item.setFont(QFont('Arial', 10, QFont.Bold))
        self.file_table.setHorizontalHeaderItem(4, header_item)

        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        # self.file_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.file_table.setFocusPolicy(Qt.NoFocus)
        self.file_table.setAlternatingRowColors(True)

        self.file_table_init()
        self.compare_file = None
        self.file_table.itemPressed.connect(self.toggle_current_radio_button)

        start_layout = QHBoxLayout()
        start_layout.addStretch(1)
        return_button = QPushButton('Return')
        compare_button = QPushButton('Compare')

        compare_button.clicked.connect(self.start_compare)
        start_layout.addWidget(return_button)
        start_layout.addWidget(compare_button)

        check_layout = QVBoxLayout()
        check_layout.addWidget(title_label)
        check_layout.addLayout(target_file_layout)
        check_layout.addWidget(self.file_table)
        check_layout.addLayout(start_layout)
        self.check_widget.setLayout(check_layout)

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

    def get_target_file(self):
        # TODO: get target file name
        return 'test.py'

    def file_table_init(self):
        # TODO: SORT BY SIMILARITY
        # TODO: color for different similarity level
        self.file_table.setRowCount(15)
        for row in range(self.file_table.rowCount()):
            radio_button = QRadioButton(f'test{row}.py')
            radio_button.setFont(QFont('Arial', 10))
            self.file_table.setCellWidget(row, 0, radio_button)
            self.file_table.setItem(row, 1, QTableWidgetItem('10KB'))
            self.file_table.setItem(row, 2, QTableWidgetItem('2021-06-01 12:00:00'))
            self.file_table.setItem(row, 3, QTableWidgetItem(f'D:/test{row}.py'))
            sim_item = QTableWidgetItem(f'{90.00 - row}%')
            sim_item.setTextAlignment(Qt.AlignCenter)
            self.file_table.setItem(row, 4, sim_item)

    def toggle_current_radio_button(self, item):
        radio_button = self.file_table.cellWidget(item.row(), 0)
        if radio_button:
            radio_button.setChecked(True)
            self.compare_file = self.file_table.item(item.row(), 3).text()

    def start_compare(self):
        if self.compare_file is None:
            QMessageBox.warning(self, 'Warning', 'Please select a file to compare first.', QMessageBox.Ok)
        else:
            print(self.compare_file)


if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    page = OneToManyPage()
    page.show()
    exit(app.exec_())
