import os
import sys
from PyQt5.QtCore import Qt, QDateTime, QFileInfo, pyqtSignal, QRect, QSize, QPoint
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor, QColor
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox, QMenu, QAction, QMessageBox, QSpinBox


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

        title_label = QLabel('<p style="color: green">一对多查重</p>')
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        
        task_name_label = QLabel('任务名称')
        task_name_label.setFont(QFont('Arial', 13, QFont.Bold))
        task_name_input = QLineEdit()
        task_name_input.setReadOnly(True)
        task_name_input.setFont(QFont('Arial', 10, QFont.Bold))
        task_name = 'Task_2024-7-26_11:18:54'
        task_name_input.setText(task_name)

        task_name_layout = QHBoxLayout()
        task_name_layout.addWidget(task_name_label)
        task_name_layout.addWidget(task_name_input)

        self.target_file_label = QLabel('目标文件')
        self.target_file_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.target_file_input = QLineEdit()
        self.target_file_input.setReadOnly(True)
        self.target_file_input.setFont(QFont('Arial', 10, QFont.Bold))
        self.target_file_input.setText(self.get_target_file())

        self.compare_file_label = QLabel('待比较文件')
        self.compare_file_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.compare_file_input = QLineEdit()
        self.compare_file_input.setText('Please select a file to compare below.')
        self.compare_file_input.setReadOnly(True)
        self.compare_file_input.setFont(QFont('Arial', 10, QFont.Bold))

        target_file_layout = QHBoxLayout()
        target_file_layout.addWidget(self.target_file_label)
        target_file_layout.addWidget(self.target_file_input)
        target_file_layout.addWidget(self.compare_file_label)
        target_file_layout.addWidget(self.compare_file_input)

        self.file_table = QTableWidget()
        # TODO: init file table items from backend
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.file_table.setColumnWidth(0, 60)

        self.file_table.setColumnCount(6)
        self.file_table.setHorizontalHeaderLabels(('名称', '大小', '上传时间', '路径', '相似度', '导出'))

        header_item = QTableWidgetItem('相似度')
        header_item.setFont(QFont('Arial', 10, QFont.Bold))
        self.file_table.setHorizontalHeaderItem(4, header_item)
        self.file_table.setStyleSheet("selection-background-color: #66BB6A")

        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.file_table.setAlternatingRowColors(True)

        self.file_table_init()
        self.compare_file = None
        self.file_table.cellClicked.connect(self.select_current_file)

        start_layout = QHBoxLayout()

        batch_export_button = QPushButton('批量导出')
        batch_export_button.clicked.connect(self.export_files)
        batch_label1 = QLabel('查重率高于')
        self.batch_spinbox = QSpinBox()
        self.batch_spinbox.setRange(0, 100)
        self.batch_spinbox.setValue(30)
        self.batch_spinbox.setSingleStep(1)
        self.batch_spinbox.setSuffix('%')
        batch_label2 = QLabel('的代码')

        start_layout.addWidget(batch_export_button)
        start_layout.addWidget(batch_label1)
        start_layout.addWidget(self.batch_spinbox)
        start_layout.addWidget(batch_label2)

        start_layout.addStretch(1)
        return_button = QPushButton('Return')
        compare_button = QPushButton('Compare')

        compare_button.clicked.connect(self.start_compare)
        start_layout.addWidget(return_button)
        start_layout.addWidget(compare_button)

        layout.addWidget(title_label)
        layout.addLayout(task_name_layout)
        layout.addLayout(target_file_layout)
        layout.addWidget(self.file_table)
        layout.addLayout(start_layout)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def get_target_file(self):
        # TODO: get target file name
        return 'test.py'

    def file_table_init(self):
        # TODO: SORT BY SIMILARITY
        # TODO: color for different similarity level
        self.file_table.setRowCount(5)
        for row in range(self.file_table.rowCount()):
            self.file_table.setItem(row, 0, QTableWidgetItem(f'test{row}.py'))
            self.file_table.setItem(row, 1, QTableWidgetItem('10KB'))
            self.file_table.setItem(row, 2, QTableWidgetItem('2021-06-01 12:00:00'))
            self.file_table.setItem(row, 3, QTableWidgetItem(f'D:/test{row}.py'))
            sim_item = QTableWidgetItem(f'{90.00 - row}%')
            sim_item.setTextAlignment(Qt.AlignCenter)
            self.file_table.setItem(row, 4, sim_item)

            widget = QWidget()
            widget_layout = QHBoxLayout()
            export_button = QPushButton()
            export_button.setIcon(QIcon('frontend/assets/Download.svg'))
            export_button.setIconSize(QSize(10, 10))
            export_button.setStyleSheet("background-color: green;border-radius: 9px")
            export_button.setFixedSize(18, 18)
            export_button.clicked.connect(self.export_file)

            widget_layout.addWidget(export_button)
            widget.setLayout(widget_layout)
            widget_layout.setContentsMargins(5, 2, 5, 2)
            self.file_table.setCellWidget(row, 5, widget)

    def export_file(self):
        x = self.sender().parentWidget().frameGeometry().x()
        y = self.sender().parentWidget().frameGeometry().y()
        row = self.file_table.indexAt(QPoint(x, y)).row()
        file_path = self.file_table.item(row, 3).text()
        print(file_path)  # TODO: export file

        filepath, _ = QFileDialog.getSaveFileName(self, "代码导出", "./", "Python (*.py)")
        # file = open(filepath, 'w')
        print(filepath)
        # file.write(txt)

    def export_files(self):
        pass

    def select_current_file(self, row, col):
        self.compare_file = self.file_table.item(row, 3).text()
        self.compare_file_input.setText(self.file_table.item(row, 0).text())

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
