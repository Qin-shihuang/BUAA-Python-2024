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
            QTableWidget {
               border-radius: 5px;
               font-size: 13px;
            }
        """)
        # self.api_client = ApiClient()

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

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(7)
        self.task_table.setHorizontalHeaderLabels(
            ['任务ID', '任务名称', '任务类型', '目标文件ID', '查重文件数', '任务提交时间', '查看'])
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.setFocusPolicy(Qt.NoFocus)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.task_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.task_table.cellDoubleClicked.connect(self.view_task)
        history_layout.addWidget(self.task_table)

        self.demo()

        return_layout = QHBoxLayout()
        return_layout.addStretch(1)
        return_button = QPushButton('  Return  ')
        # TODO: return_button.clicked.connect(self.switch_to_welcome_page)
        return_layout.addWidget(return_button)
        history_layout.addLayout(return_layout)

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

    def demo(self):
        for row in range(100):
            self.task_table.insertRow(row)
            for col in range(7):
                self.task_table.setItem(row, col, QTableWidgetItem(f'{row} - {col}'))
                if col == 6:
                    view_widget = QWidget()
                    view_layout = QHBoxLayout()
                    view_widget.setLayout(view_layout)
                    view_button = QPushButton('View')
                    view_button.setStyleSheet(
                        'padding: 5px; background-color: #4CAF50; color: white; border: none; border-radius: 11px;')
                    view_button.clicked.connect(self.view_task_for_button)
                    view_layout.addWidget(view_button)
                    view_layout.setContentsMargins(5, 5, 5, 5)
                    self.task_table.setCellWidget(row, col, view_widget)

    def get_task_infos(self):
        pass
        # status, tasks = self.api_client.GetTaskList()
        # if status != ErrorCode.SUCCESS:
        #     QMessageBox.critical(self, 'Error', 'Failed to get history tasks')
        #     return
        # for task in tasks:
        #     row = self.task_table.rowCount()
        #     self.task_table.insertRow(row)
        #     self.task_table.setItem(row, 0, QTableWidgetItem(task[0]))
        #     self.task_table.setItem(row, 1, QTableWidgetItem(task[1]))
        #     if task[2] == 0:
        #         self.task_table.setItem(row, 2, QTableWidgetItem('one-to-many'))
        #         self.task_table.setItem(row, 3, QTableWidgetItem(task[3]))
        #     else:
        #         self.task_table.setItem(row, 2, QTableWidgetItem('many-to-many'))
        #         self.task_table.setItem(row, 3, QTableWidgetItem('-----'))
        #     self.task_table.setItem(row, 4, QTableWidgetItem(task[4]))
        #     self.task_table.setItem(row, 5, QTableWidgetItem(task[5]))
        #     view_widget = QWidget()
        #     view_layout = QHBoxLayout()
        #     view_widget.setLayout(view_layout)
        #     view_button = QPushButton('View')
        #     view_button.setStyleSheet(
        #         'padding: 5px; background-color: #4CAF50; color: white; border: none; border-radius: 11px;')
        #     view_button.clicked.connect(self.view_task_for_button)
        #     view_layout.addWidget(view_button)
        #     view_layout.setContentsMargins(5, 5, 5, 5)
        #     self.task_table.setCellWidget(row, 6, view_widget)

    def view_task_for_button(self):
        x = self.sender().parentWidget().frameGeometry().x()
        y = self.sender().parentWidget().frameGeometry().y()
        row = self.task_table.indexAt(QPoint(x, y)).row()
        task_id = self.task_table.item(row, 0).text()
        print('View task' + task_id)

    def view_task(self, row, col):
        task_id = self.task_table.item(row, 0).text()
        print('View task' + task_id)


if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    history_page = HistoryPage()
    history_page.show()
    exit(app.exec_())
