import multiprocessing
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer

class ProgressWidget(QWidget):    
    def __init__(self, desp, total):
        super().__init__()
        self.setWindowTitle("Progress")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedSize(400, 100)
        self.center()
        
        layout = QVBoxLayout()
        info_area = QHBoxLayout()
        desp_label = QLabel(desp)
        self.progress_label = QLabel(f"0/{total}")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        info_area.addWidget(desp_label)
        info_area.addWidget(self.progress_label)
        layout.addLayout(info_area)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(total)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.progress_value = multiprocessing.Value('i', 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # 每100ms更新一次进度
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def update_progress(self):
        progress = self.progress_value.value
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"{progress}/{self.progress_bar.maximum()}")
        if progress >= self.progress_bar.maximum() or progress == -1:
            self.close()

def run_progress_widget(desp, total, progress_value):
    app = QApplication([])
    progress_widget = ProgressWidget(desp, total)
    progress_widget.progress_value = progress_value
    progress_widget.show()
    app.exec_()

class ProgressSignal:
    def __init__(self, progress_value):
        self.progress_value = progress_value

    def emit(self, progress):
        self.progress_value.value = progress

def start_progress_widget(desp, total):
    progress_value = multiprocessing.Value('i', 0)
    process = multiprocessing.Process(target=run_progress_widget, args=(desp, total, progress_value))
    process.start()
    return ProgressSignal(progress_value)
