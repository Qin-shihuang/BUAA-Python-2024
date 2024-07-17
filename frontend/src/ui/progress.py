from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject

class ProgressSignal(QObject):
    update = pyqtSignal(int)

class ProgressWindow(QWidget):    
    def __init__(self, desp, total):
        super().__init__()
        self.setWindowTitle("Progress")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 100)
        self.center()
        
        layout = QVBoxLayout()
        info_area = QHBoxLayout()
        desp_label = QLabel(desp)
        self.progress_label = QLabel(f"0/{total}")
        info_area.addWidget(desp_label)
        info_area.addWidget(self.progress_label)
        layout.addLayout(info_area)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(total)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"{progress}/{self.progress_bar.maximum()}")
        