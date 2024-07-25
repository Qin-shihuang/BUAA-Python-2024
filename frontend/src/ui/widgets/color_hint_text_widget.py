from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QSize, QRect

class ColorHintTextWidget(QWidget):
    def __init__(self, text, color, parent=None):
        super().__init__(parent)
        self.text = text
        self.color = color
        
        self.label = QLabel(text)
        self.label.setContentsMargins(20, 0, 0, 0)
        self.label.setAlignment(Qt.AlignVCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        height = self.height()
        square_size = 20
        y = (height - square_size) // 2
        rect = QRect(5, y, square_size, square_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRoundedRect(rect, 5, 5)
        
    def sizeHint(self):
        return QSize(100, 40)
    
