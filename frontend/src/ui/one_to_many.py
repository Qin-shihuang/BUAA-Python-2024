import os
import sys
from PyQt5.QtCore import Qt, QDateTime, QFileInfo, pyqtSignal, QRect, QSize, QPoint, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor, QColor
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox, QMenu, QAction, QMessageBox, QSpinBox, \
    QDoubleSpinBox, QProgressBar, QFrame, QScrollArea, QScrollBar, QSizePolicy, QAbstractScrollArea, QSlider

from models.report_model import ReportModel
from utils.api_client import ApiClient
from utils.error_codes import ErrorCode
from utils.info_container import InfoContainer


class OneToManyPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome")
        self.resize(900, 600)
        self.center()

        self.api_client = ApiClient()
        self.info_container = InfoContainer()
        
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
        self.task_name_input = QLineEdit()
        self.task_name_input.setReadOnly(True)
        self.task_name_input.setFont(QFont('Arial', 10, QFont.Bold))
        
        task_name_layout = QHBoxLayout()
        task_name_layout.addWidget(task_name_label)
        task_name_layout.addWidget(self.task_name_input)

        self.target_file_label = QLabel('目标文件')
        self.target_file_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.target_file_input = QLineEdit()
        self.target_file_input.setReadOnly(True)
        self.target_file_input.setFont(QFont('Arial', 10, QFont.Bold))

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
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.file_table.setColumnWidth(0, 60)

        self.file_table.setColumnCount(7)
        self.file_table.setHorizontalHeaderLabels(('名称', '大小', '上传时间', '路径', '相似距离', '导出', 'ID'))
        # self.file_table.setColumnHidden(6, True)

        header_item = QTableWidgetItem('相似距离')
        header_item.setFont(QFont('Arial', 10, QFont.Bold))
        self.file_table.setHorizontalHeaderItem(4, header_item)
        self.file_table.setStyleSheet("selection-background-color: #66BB6A")

        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.file_table.setAlternatingRowColors(True)

        # self.file_table_init()
        self.compare_file = None
        self.file_table.cellClicked.connect(self.select_current_file)
        self.file_table.cellDoubleClicked.connect(self.start_compare)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel('                             '))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(1)
        self.slider.setSingleStep(1)
        self.slider.setFixedWidth(150)
        self.slider.setVisible(False)
        self.slider.valueChanged.connect(lambda: self.lineEdit.setText(str(self.slider.value()/100)))
        slider_layout.addWidget(self.slider)
        slider_layout.addStretch(1)

        start_layout = QHBoxLayout()

        batch_export_button = QPushButton('批量导出')
        batch_export_button.clicked.connect(self.export_files)
        batch_label1 = QLabel('相似距离低于')
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedSize(60, 30)
        self.lineEdit.setStyleSheet("padding: 1px;")
        self.lineEdit.setFont(QFont('Arial', 10))
        batch_label2 = QLabel('的代码')

        self.lineEdit.installEventFilter(self)
        self.slider.installEventFilter(self)
        self.sliderHovered = False
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.checkMousePosition)

        start_layout.addWidget(batch_export_button)
        start_layout.addWidget(batch_label1)
        start_layout.addWidget(self.lineEdit)
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
        layout.addLayout(slider_layout)
        layout.addLayout(start_layout)

    def eventFilter(self, source, event):
        if source == self.lineEdit or source == self.slider:
            if event.type() == event.Enter:
                self.slider.setVisible(True)
                self.sliderHovered = True
                self.timer.stop()  # 停止隐藏定时器
            elif event.type() == event.Leave:
                self.sliderHovered = False
                self.timer.start(500)  # 设定一个短暂的延迟时间以判断鼠标是否离开组件
        return super(QWidget, self).eventFilter(source, event)

    def checkMousePosition(self):
        # 检查鼠标是否在lineEdit或slider区域内
        if not (self.lineEdit.underMouse() or self.slider.underMouse()):
            self.slider.setVisible(False)
    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

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
            export_button.setIcon(QIcon('assets/Download.svg'))
            export_button.setIconSize(QSize(10, 10))
            export_button.setStyleSheet("background-color: green;border-radius: 9px")
            export_button.setFixedSize(18, 18)
            export_button.clicked.connect(self.export_file)

            widget_layout.addWidget(export_button)
            widget.setLayout(widget_layout)
            widget_layout.setContentsMargins(5, 2, 5, 2)
            self.file_table.setCellWidget(row, 5, widget)
    
    def init_task(self, task_name, task):
        self.task_name_input.setText(task_name)
        self.target_file_input.setText(self.info_container.get_file_name(task.mainFileId))
        for report_id in task.reportIds:
            with open(f'src/cache/reports/report_{report_id}.json', 'r') as f:
                report = ReportModel.fromJson(f.read())

            if report.file1Id == task.mainFileId:
                file_id = report.file2Id
            else:
                file_id = report.file1Id
            file_info = self.info_container.get_file_info(file_id)
            row = self.file_table.rowCount()
            self.file_table.insertRow(row)
            self.file_table.setItem(row, 0, QTableWidgetItem(file_info[0]))

            size = file_info[1]
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size / 1024 / 1024:.2f} MB"

            self.file_table.setItem(row, 1, QTableWidgetItem(size_str))
            self.file_table.setItem(row, 2, QTableWidgetItem(file_info[3]))
            self.file_table.setItem(row, 3, QTableWidgetItem(file_info[2]))
            self.file_table.setItem(row, 6, QTableWidgetItem(str(file_id)))

            sim_item = QTableWidgetItem(f'{report.distance}')
            sim_item.setTextAlignment(Qt.AlignCenter)
            self.file_table.setItem(row, 4, sim_item)

            widget = QWidget()
            widget_layout = QHBoxLayout()
            export_button = QPushButton()
            export_button.setIcon(QIcon('assets/Download.svg'))
            export_button.setIconSize(QSize(10, 10))
            export_button.setStyleSheet("background-color: green;border-radius: 9px")
            export_button.setFixedSize(18, 18)
            export_button.clicked.connect(self.export_file)

            widget_layout.addWidget(export_button)
            widget.setLayout(widget_layout)
            widget_layout.setContentsMargins(5, 2, 5, 2)
            self.file_table.setCellWidget(row, 5, widget)

        # self.file_table.setSortingEnabled(True)
        # self.file_table.sortItems(4, Qt.DescendingOrder)
        self.file_table.sortItems(4, Qt.AscendingOrder)
        # need to reload op...

    def export_file(self):
        x = self.sender().parentWidget().frameGeometry().x()
        y = self.sender().parentWidget().frameGeometry().y()
        row = self.file_table.indexAt(QPoint(x, y)).row()
        file_id = int(self.file_table.item(row, 6).text())
        file_name = self.file_table.item(row, 0).text()
        filepath, _ = QFileDialog.getSaveFileName(self, "代码导出", f"./{file_name}", "Python (*.py)")

        if not filepath:
            return
        if not os.path.exists(f'src/cache/files/file_{file_id}.py'):
            _, file_content = self.api_client.download_file(file_id)
            if _ == ErrorCode.SUCCESS:
                with open(filepath, 'wb') as f:
                    f.write(file_content)
            else:
                QMessageBox.critical(self, 'Error', 'Failed to get file!')
        else:
            with open(f'src/cache/files/file_{file_id}.py', 'r') as f:
                file_content = f.read()
            with open(filepath, 'w') as f:
                f.write(file_content)

    def export_files(self):
        thres = self.lineEdit.value()

        file_ids = []
        # for row in range(self.file_table.rowCount()):
        #     similarity = float(self.file_table.item(row, 4).text()[:-1])
        #     if similarity > thres:
        #         file_ids.append(int(self.file_table.item(row, 6).text()))
        #     else:
        #         break
        
        # if not file_ids:
        #     QMessageBox.warning(self, 'Warning', 'No files to export.', QMessageBox.Ok)
        #     return
        
        dirpath = QFileDialog.getExistingDirectory(self, "代码导出目录", "./", QFileDialog.ShowDirsOnly)

        return
        for file_id in file_ids:
            if not os.path.exists(f'src/cache/files/file_{file_id}.py'):
                _, file_content = self.api_client.download_file(file_id)
                if _ == ErrorCode.SUCCESS:
                    with open(dirpath + '/' + self.info_container.get_file_name(file_id), 'wb') as f:
                        f.write(file_content)
                else:
                    QMessageBox.critical(self, 'Error', 'Failed to get file!')
            else:
                with open(f'src/cache/files/file_{file_id}.py', 'r') as f:
                    file_content = f.read()
                with open(dirpath + '/' + self.info_container.get_file_name(file_id), 'w') as f:
                    f.write(file_content)
        

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
