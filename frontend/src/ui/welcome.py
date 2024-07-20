import os
import sys
from PyQt5.QtCore import Qt, QDateTime, QFileInfo, pyqtSignal, QRect, QSize, QPoint
from PyQt5.QtGui import QFont, QIcon, QPixmap
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox


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
            QScrollBar:vertical{
                background:#f0f0f0;
                padding:0px;
                border-radius:20px;
                max-width:12px;
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
        self.task_name_input.setText(self.get_default_name())
        reset_task_name_button = QPushButton('重置任务名')
        reset_task_name_button.clicked.connect(lambda: self.task_name_input.setText(self.get_default_name()))
        task_name_layout = QHBoxLayout()
        task_name_layout.addWidget(self.task_name_label)
        task_name_layout.addWidget(self.task_name_input)
        task_name_layout.addWidget(reset_task_name_button)

        self.file_label = QLabel('上传待查文件')
        self.upload_file_button = QPushButton('上传文件')
        self.upload_file_button.clicked.connect(self.upload_file)
        clear_file_button = QPushButton('清空已上传文件')
        clear_file_button.clicked.connect(self.clear_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.upload_file_button)
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
        self.target_file_label = QLabel('选择目标文件(仅一对多查重模式)<sup style="color: red">*</sup>')
        self.target_file_combobox = QComboBox()
        self.target_file_combobox.addItem('请选择目标文件')
        self.target_file_combobox.currentIndexChanged.connect(lambda: self.target_file_label.setStyleSheet("color: black"))

        self.target_layout.addWidget(self.target_file_label)
        self.target_layout.addWidget(self.target_file_combobox)

        self.file_table = QTableWidget()
        # TODO: init file table items from backend
        self.file_table.setStyleSheet("QTableWidget{font-size:13px;}")
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.file_table.setHorizontalHeader(CheckBoxHeader(combobox=self.target_file_combobox))
        # self.file_table.setColumnWidth(0, 60)

        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(('     名称 ', '大小', '上传时间', '  路径  ', '操作'))
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.file_table.setFocusPolicy(Qt.NoFocus)
        self.file_table.setAlternatingRowColors(True)

        self.file_table.cellClicked.connect(self.toggle_current_checkbox)

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
        upload_layout.addWidget(self.file_table)
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

    def get_default_name(self):
        datetime = QDateTime.currentDateTime()
        time = list(datetime.toString().split())[3]
        year = datetime.date().year()
        month = datetime.date().month()
        day = datetime.date().day()
        return 'Task_' + str(year) + '-' + str(month) + '-' + str(day) + '_' + time

    def get_current_time(self):
        datetime = QDateTime.currentDateTime()
        time = list(datetime.toString().split())[3]
        year = datetime.date().year()
        month = datetime.date().month()
        day = datetime.date().day()
        return str(year) + '-' + str(month) + '-' + str(day) + ' ' + time

    def task_name_lost_focus(self, event):
        if self.task_name_input.text() != '':
            self.task_name_label.setStyleSheet("color: black")
            self.error_label.clear()

    def toggle_current_checkbox(self):
        item = self.file_table.item(self.file_table.currentRow(), 0)
        if item.checkState() == Qt.Checked:
            self.target_file_combobox.removeItem(self.target_file_combobox.findText(item.text()))
            item.setCheckState(Qt.Unchecked)
        else:
            self.target_file_combobox.addItem(item.text())
            item.setCheckState(Qt.Checked)

    def upload_file(self):
        self.files, _ = QFileDialog.getOpenFileNames(self, "请选择待查重代码", "./", "Python (*.py)")
        current_time = self.get_current_time()
        for file in self.files:
            info = QFileInfo(file)
            row = self.file_table.rowCount()
            self.file_table.insertRow(row)
            # self.file_table.setSortingEnabled(True)

            checkbox = QTableWidgetItem(info.fileName())
            checkbox.setCheckState(Qt.Unchecked)
            self.file_table.setItem(row, 0, checkbox)
            self.file_table.setItem(row, 1, QTableWidgetItem(str('{:.1f}'.format(info.size() / 1024)) + 'KB'))
            self.file_table.setItem(row, 2, QTableWidgetItem(current_time))
            self.file_table.setItem(row, 3, QTableWidgetItem(info.filePath()))

            widget = QWidget()
            widget_layout = QHBoxLayout()

            open_button = QPushButton()
            open_button.setIcon(QIcon('frontend/src/ui/icons/Open.svg'))
            open_button.setIconSize(QSize(10, 10))
            open_button.setStyleSheet("background-color: green;border-radius: 9px")
            open_button.setFixedSize(18, 18)
            open_button.clicked.connect(self.open_file)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon('frontend/src/ui/icons/Delete.svg'))
            delete_button.setIconSize(QSize(10, 10))
            delete_button.setStyleSheet("background-color: red;border-radius: 9px")
            delete_button.setFixedSize(18, 18)
            delete_button.clicked.connect(self.delete_file)

            widget_layout.addWidget(open_button)
            widget_layout.addWidget(delete_button)
            widget.setLayout(widget_layout)
            widget_layout.setContentsMargins(5, 2, 5, 2)
            self.file_table.setCellWidget(row, 4, widget)

        if self.file_table.rowCount() > 0:
            self.file_label.setStyleSheet("color: black")
            self.error_label.clear()
        # if filename:
        #     with open(filename, 'r') as f:
        #         text = f.read()
        #     self.textedit.setText(text)

    def clear_file(self):
        self.file_table.clearContents()
        self.file_table.setRowCount(0)
        self.target_file_combobox.clear()
        self.target_file_combobox.addItem('请选择目标文件')

    def open_file(self):
        # TODO: open file from backend, view in code editor
        x = self.sender().parentWidget().frameGeometry().x()
        y = self.sender().parentWidget().frameGeometry().y()
        row = self.file_table.indexAt(QPoint(x, y)).row()
        file_path = self.file_table.item(row, 3).text()
        print(file_path)

    def delete_file(self):
        # TODO: delete file from backend
        x = self.sender().parentWidget().frameGeometry().x()
        y = self.sender().parentWidget().frameGeometry().y()
        row = self.file_table.indexAt(QPoint(x, y)).row()
        if self.file_table.item(row, 0).checkState() == Qt.Checked:
            self.target_file_combobox.removeItem(
                self.target_file_combobox.findText(self.file_table.item(row, 0).text()))
        self.file_table.removeRow(row)

    def switch_mode(self):
        sender = self.sender()
        self.mode_select_label.setStyleSheet("color: black")
        self.error_label.clear()
        if sender.text() == '一对多查重':
            if sender.isChecked():
                self.check_mode = 0
                self.upload_widget.layout().insertLayout(5, self.target_layout)
                self.target_file_combobox.show()
                self.target_file_label.show()
            else:
                self.target_file_combobox.hide()
                self.target_file_label.hide()
                self.upload_widget.layout().removeItem(self.target_layout)
        elif sender.text() == '组内自查':
            if sender.isChecked():
                self.check_mode = 1

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
        elif not self.file_table.rowCount() > 0:
            self.file_label.setStyleSheet("color: red")
            self.error_label.setText('请上传待查文件')
            return
        elif self.check_mode is None:
            self.mode_select_label.setStyleSheet("color: red")
            self.error_label.setText('请选择查重模式')
            return
        elif self.check_mode == 0 and self.target_file_combobox.currentText() == '请选择目标文件':
            self.target_file_label.setStyleSheet("color: red")
            self.error_label.setText('请选择目标文件')
            return
        self.error_label.setStyleSheet("color: green")
        self.error_label.setText('Success!')
        # enter code editor...
        files = []
        for row in range(self.file_table.rowCount()):
            if self.file_table.item(row, 0).checkState() == Qt.Checked:
                files.append(self.file_table.item(row, 3).text())
        target_file = self.target_file_combobox.currentText()
        print(target_file, files)


class CheckBoxHeader(QHeaderView):
    select_all_clicked = pyqtSignal(bool)

    def __init__(self, orientation=Qt.Horizontal, parent=None, combobox=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False
        self.select_all_clicked.connect(self.toggle_all_checkboxes)
        self.target_file_combobox = combobox

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(3, 5, 10, 10)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            if self.isOn:
                self.isOn = False
            else:
                self.isOn = True
            self.select_all_clicked.emit(self.isOn)
            self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    def toggle_all_checkboxes(self, check):
        table = self.parent()
        self.target_file_combobox.clear()
        self.target_file_combobox.addItem('请选择目标文件')
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if check:
                item.setCheckState(Qt.Checked)
                self.target_file_combobox.addItem(item.text())
            else:
                item.setCheckState(Qt.Unchecked)


if __name__ == "__main__":
    PyQt5.QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    welcome_page = WelcomePage()
    welcome_page.show()

    exit(app.exec_())
