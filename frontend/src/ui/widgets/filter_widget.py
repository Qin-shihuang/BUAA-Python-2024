from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath

class FilterWidget(QWidget):
    def __init__(self, filteredChangedSignal=None):
        super().__init__()
        self.values = []
        self.old_threshold = 0.0
        self.threshold = 0.0
        self.selectSmaller = True
        self.dragging = False
        self.display_area = self
        self.display_area.setMouseTracking(True)
        self.signal = filteredChangedSignal
        
    def setup(self, values, threshold=0.25, selectSmaller=True):
        # values: List[Tuple(int, int, float)]
        self.values = values
        self.old_threshold = threshold
        self.threshold = threshold
        self.selectSmaller = selectSmaller
        if self.signal:
            self.signal.emit(self._filter())
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        
        slider_width = 20
        slider_height = 25
        triangle_height = 10
        
        bar_height = height - slider_height
        y = 0
        
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRect(QRectF(0, y, width, bar_height))  
        
        for _, _, value in self.values:
            x = int(value * width)
            if value <= self.threshold:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
            else:
                painter.setPen(QPen(QColor(0, 255, 0), 2))
            painter.drawLine(x, y, x, y + bar_height)  
            
        slider_x = int(self.threshold * width)
            
        path = QPainterPath()
        path.moveTo(slider_x, y + bar_height)
        path.lineTo(slider_x - slider_width/2, y + bar_height + triangle_height)
        path.lineTo(slider_x - slider_width/2, y + bar_height + slider_height - 5)
        path.arcTo(slider_x - slider_width/2, y + bar_height + slider_height - 10, 10, 10, 180, 90)
        path.lineTo(slider_x + slider_width/2 - 5, y + bar_height + slider_height)
        path.arcTo(slider_x + slider_width/2 - 10, y + bar_height + slider_height - 10, 10, 10, 270, 90)
        path.lineTo(slider_x + slider_width/2, y + bar_height + triangle_height)
        path.closeSubpath()
            
        painter.setBrush(QBrush(QColor(60, 60, 200, 200)))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        painter.setPen(QPen(QColor(60, 60, 200), 2, Qt.DashLine))
        painter.drawLine(slider_x, y, slider_x, y + bar_height)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.updateThreshold(event.x() / self.width())
            self.dragging = True
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.updateThreshold(event.x() / self.width())
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            if self.old_threshold != self.threshold:
                self.old_threshold = self.threshold
                if self.signal:
                    self.signal.emit(self._filter())
                
    def updateThreshold(self, value):
        self.threshold = max(0, min(1, value))
        self.update()

    def _filter(self):
        if not self.values:
            return []
        if self.selectSmaller:
            return [v for v in self.values if v[2] <= self.threshold]
        else:
            return [v for v in self.values if v[2] >= self.threshold]
        
def signal_handler(values):
    print(values)

class FilterSignal(QObject):
    update = pyqtSignal(list)
    
    def emit(self, values):
        self.update.emit(values)
        
    def connect(self, callback):
        self.update.connect(callback)
    