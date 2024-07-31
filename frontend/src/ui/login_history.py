from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QLabel, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.api_client import ApiClient
from utils.error_codes import ErrorCode

class LoginHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Login History")
        layout = QVBoxLayout()
        self.last_login_label = QLabel()
        self.last_login_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.last_login_label.setStyleSheet("color: green")
        self.login_history_widget = QTableWidget()
        self.login_history_widget.setColumnCount(2)
        self.login_history_widget.setHorizontalHeaderLabels(['Time', 'Status'])
        self.login_history_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.login_history_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.login_history_widget.setAlternatingRowColors(True)
        self.login_history_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.login_history_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.login_history_widget.setStyleSheet("selection-background-color: #66BB6A")

        layout.addWidget(self.last_login_label)
        layout.addWidget(self.login_history_widget)
        self.setLayout(layout)
        self.api_client = ApiClient()

    def show(self):
        self.update()
        super().show()

    def update(self):
        self.login_history_widget.setRowCount(0)
        status, record = self.api_client.get_login_history(limit = -1)
        if status == ErrorCode.SUCCESS:
            if len(record) == 1:
                self.last_login_label.setText("First login!")
            else:
                # we need to skip the first record because it's the current login
                login_time = record[1][0]
                self.last_login_label.setText(f"Last login: {login_time}")
            for row in record:
                time_item = QTableWidgetItem(row[0])
                time_item.setTextAlignment(Qt.AlignCenter)
                status_item = QTableWidgetItem('Succeeded' if row[1] == True else 'Failed')
                status_item.setTextAlignment(Qt.AlignCenter)
                i = self.login_history_widget.rowCount()
                self.login_history_widget.insertRow(i)
                self.login_history_widget.setItem(i, 0, time_item)
                self.login_history_widget.setItem(i, 1, status_item)
        else:
            self.last_login_label.setText("Failed to get login history")
            self.login_history_widget.setRowCount(0)
        