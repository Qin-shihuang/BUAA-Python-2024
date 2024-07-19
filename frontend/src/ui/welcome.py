import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget


class WelcomePage(QWidget):
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

        self.stack_widget = QStackedWidget()
        layout.addWidget(self.stack_widget)

        # --------------------stack_widget_0------------------- #
        self.upload_widget = QWidget()

        title_label = QLabel('<p style="color: green">上传待查代码</p>')
        title_label.setFont(QFont('Arial', 20, QFont.Bold))

        self.task_name_label = QLabel('查重任务名')
        self.task_name_input = QLineEdit()
        self.task_name_input.focusOutEvent = self.task_name_lost_focus
        self.task_name_input.setPlaceholderText('请输入本次查重任务名称')
        task_name_layout = QHBoxLayout()
        task_name_layout.addWidget(self.task_name_label)
        task_name_layout.addWidget(self.task_name_input)

        self.file_label = QLabel('上传待查文件')
        self.files = []
        self.select_file_button = QPushButton('选择文件')
        self.select_file_button.clicked.connect(self.select_file)
        clear_file_button = QPushButton('清除已选择文件')
        clear_file_button.clicked.connect(self.clear_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.select_file_button)
        file_layout.addWidget(clear_file_button)

        self.mode_select_label = QLabel('选择查重模式')
        self.check_mode = None
        one2many_button = QRadioButton('一对多查重')
        group_button = QRadioButton('组内自查')
        one2many_button.toggled.connect(self.switch_mode)
        group_button.toggled.connect(self.switch_mode)
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.mode_select_label)
        mode_layout.addWidget(one2many_button)
        mode_layout.addWidget(group_button)

        self.target_layout = QHBoxLayout()
        self.target_file_label = QLabel('选择目标文件(仅一对多查重模式)')
        self.target_file_button = QPushButton('请在列表中选择目标文件')
        self.target_file_button.setCheckable(False)
        self.target_layout.addWidget(self.target_file_label)
        self.target_layout.addWidget(self.target_file_button)

        self.file_sheet = QListWidget()
        self.file_sheet.setStyleSheet("QListWidget{font-size:16px;}");
        self.file_sheet.itemSelectionChanged.connect(self.set_target_file)

        start_layout = QHBoxLayout()
        self.error_label = QLabel()
        self.error_label.setObjectName("error_label")
        self.error_label.setStyleSheet("color: red")
        start_layout.addWidget(self.error_label)
        start_layout.addStretch(1)
        history_button = QPushButton('查看历史查重任务')
        start_button = QPushButton('开始查重')
        history_button.clicked.connect(self.show_history)
        start_button.clicked.connect(self.start_check)
        start_layout.addWidget(history_button)
        start_layout.addWidget(start_button)

        upload_layout = QVBoxLayout()
        upload_layout.addWidget(title_label)
        upload_layout.addLayout(task_name_layout)
        upload_layout.addLayout(file_layout)
        upload_layout.addLayout(mode_layout)
        upload_layout.addWidget(self.file_sheet)
        upload_layout.addLayout(start_layout)
        self.upload_widget.setLayout(upload_layout)

        self.stack_widget.addWidget(self.upload_widget)

        # --------------------stack_widget_1------------------- #
        self.history_widget = QWidget()
        history_title_label = QLabel('<p style="color: green">历史查重任务</p>')
        history_title_label.setFont(QFont('Arial', 20, QFont.Bold))

        history_layout = QVBoxLayout()
        history_layout.addWidget(history_title_label)
        self.history_widget.setLayout(history_layout)

        self.stack_widget.addWidget(self.history_widget)
        # tmp
        tmp_btn = QPushButton('return')
        history_layout.addWidget(tmp_btn)
        tmp_btn.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))

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

    def task_name_lost_focus(self, event):
        if self.task_name_input.text() != '':
            self.task_name_label.setStyleSheet("color: black")
            self.error_label.clear()

    def select_file(self):
        self.file_sheet.clear()
        self.files, _ = QFileDialog.getOpenFileNames(self, "请选择待查重代码", "./", "Python (*.py)")
        for file in self.files:
            self.file_sheet.addItem(os.path.basename(file))
        self.target_file_button.setText('请在列表中选择目标文件')
        if self.files:
            self.file_label.setStyleSheet("color: black")
            self.error_label.clear()
        # if filename:
        #     with open(filename, 'r') as f:
        #         text = f.read()
        #     self.textedit.setText(text)

    def clear_file(self):
        self.file_sheet.clear()
        self.target_file_button.setText('请在列表中选择目标文件')

    def switch_mode(self):
        sender = self.sender()
        self.mode_select_label.setStyleSheet("color: black")
        self.error_label.clear()
        if sender.text() == '一对多查重':
            if sender.isChecked():
                self.check_mode = 0
                self.upload_widget.layout().insertLayout(4, self.target_layout)
                self.target_file_button.show()
                self.target_file_label.show()
            else:
                self.target_file_button.hide()
                self.target_file_label.hide()
                self.upload_widget.layout().removeItem(self.target_layout)
        elif sender.text() == '组内自查':
            if sender.isChecked():
                self.check_mode = 1

    def set_target_file(self):
        self.target_file_button.setText(self.file_sheet.currentItem().text())
        self.target_file_label.setStyleSheet("color: black")
        self.error_label.clear()

    def show_history(self):
        self.task_name_label.setStyleSheet("color: black")
        self.file_label.setStyleSheet("color: black")
        self.mode_select_label.setStyleSheet("color: black")
        self.target_file_label.setStyleSheet("color: black")
        self.error_label.clear()
        self.stack_widget.setCurrentIndex(1)

    def start_check(self):
        self.error_label.setStyleSheet("color: red")
        if self.task_name_input.text() == '':
            self.task_name_label.setStyleSheet("color: red")
            self.error_label.setText('任务名不能为空')
            return
        elif not self.files:
            self.file_label.setStyleSheet("color: red")
            self.error_label.setText('请上传待查文件')
            return
        elif self.check_mode is None:
            self.mode_select_label.setStyleSheet("color: red")
            self.error_label.setText('请选择查重模式')
            return
        elif self.check_mode == 0 and self.target_file_button.text() == '请在列表中选择目标文件':
            self.target_file_label.setStyleSheet("color: red")
            self.error_label.setText('请选择目标文件')
            return
        self.error_label.setStyleSheet("color: green")
        self.error_label.setText('Success!')
        # enter code editor...


if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    welcome_page = WelcomePage()
    welcome_page.show()

    exit(app.exec_())
