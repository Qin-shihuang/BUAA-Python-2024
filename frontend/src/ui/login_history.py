from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from utils.api_client import ApiClient
from utils.error_codes import ErrorCode

class LoginHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        layout = QVBoxLayout()
        self.last_login_label = QLabel()
        self.login_history_widget = QTableWidget()
        self.login_history_widget.setColumnCount(2)
        self.login_history_widget.setHorizontalHeaderLabels(['Time', 'Status'])
        self.login_history_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.login_history_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.last_login_label)
        layout.addWidget(self.login_history_widget)
        self.setLayout(layout)
        self.api_client = ApiClient()

    def show(self):
        self.update()
        super().show()

    def update(self):
        status, record = self.api_client.get_login_history(limit = -1)
        if status == ErrorCode.SUCCESS:
            # we need to skip the first record because it's the current login
            login_time = record[1][0]
            self.last_login_label.setText(f"Last  login: {login_time}")
            for row in record:
                time_item = QTableWidgetItem(row[0])
                status_item = QTableWidgetItem('Succeeded' if row[1] == True else 'Failed')
                i = self.login_history_widget.rowCount()
                self.login_history_widget.insertRow(i)
                self.login_history_widget.setItem(i, 0, time_item)
                self.login_history_widget.setItem(i, 1, status_item)
        else:
            self.last_login_label.setText("Failed to get login history")
            self.login_history_widget.setRowCount(0)
        