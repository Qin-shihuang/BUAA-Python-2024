from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QApplication,
                             QScrollArea, QGridLayout)
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QResizeEvent, QColor

class DynamicCheckboxWidget(QWidget):
    def __init__(self, checkboxChangedSignal=None):
        super().__init__()
        self.checkboxes = []
        self.checked_indices = []
        self.checkboxChangedSignal = checkboxChangedSignal
        
        main_layout = QVBoxLayout()
        
        self.checkbox_container = QWidget()
        self.checkbox_layout = QGridLayout(self.checkbox_container)
        self.checkbox_layout.setSpacing(5)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.checkbox_container)
        
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def setup(self, n, colors):
        for i in range(n):
            checkbox = QCheckBox(f"Cluster {i}")
            color = colors[i % len(colors)]
            checkbox.setStyleSheet(self._get_checkbox_style(color))
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox, i, 0)
            self.checked_indices.append(i)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda checked, i=i: self.on_checkbox_changed(i, checked))
        self._adjust_layout()
        if self.checkboxChangedSignal:
            self.checkboxChangedSignal.emit(self.checked_indices)
        
    def _get_checkbox_style(self, color: QColor):
        return f"""
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
                border: 2px solid #999999;
                border-radius: 4px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {color.name()};
                background: {color.name()};
            }}
            QCheckBox::indicator:hover {{
                border-color: {color.darker(120).name()};
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: {color.darker(120).name()};
            }}
        """
        
    def _adjust_layout(self):
        for i in reversed(range(self.checkbox_layout.count())): 
            self.checkbox_layout.itemAt(i).widget().setParent(None)
            
        checkbox_width = 50
        container_width = self.checkbox_container.width()
        checkboxes_per_row = max(1, container_width // checkbox_width)
        
        for i, checkbox in enumerate(self.checkboxes):
            row = i // checkboxes_per_row
            col = i % checkboxes_per_row
            self.checkbox_layout.addWidget(checkbox, row, col)
        
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        QTimer.singleShot(0, self._adjust_layout)
        
    def on_checkbox_changed(self, index, checked):
        if checked:
            self.checked_indices.append(index)
        else:
            self.checked_indices.remove(index)
        
        if self.checkboxChangedSignal:
            self.checkboxChangedSignal.emit(self.checked_indices)
        
class CheckboxChangedSignal(QObject):
    signal = pyqtSignal(list)
    
    def emit(self, indices):
        self.signal.emit(indices)
        
    def connect(self, callback):
        self.signal.connect(callback)
        
def signal_handler(checked):
    print(checked)
        
if __name__ == '__main__':
    app = QApplication([])
    sig = CheckboxChangedSignal()
    sig.connect(signal_handler)
    window = DynamicCheckboxWidget(sig)
    colors = [QColor("#3498db"), QColor("#e74c3c"), QColor("#2ecc71"), QColor("#f39c12")]
    window.setup(4, colors)
    window.show()
    exit(app.exec_())