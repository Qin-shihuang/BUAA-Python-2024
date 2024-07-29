import networkx as nx
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, QObject
from random import randint


CLUSTER_COLORS = [
    QColor(31, 119, 180), 
    QColor(255, 127, 14), 
    QColor(44, 160, 44),  
    QColor(214, 39, 40),  
    QColor(148, 103, 189),
    QColor(140, 86, 75),  
    QColor(227, 119, 194),
    QColor(127, 127, 127),
    QColor(188, 189, 34), 
    QColor(23, 190, 207)
]

class GraphWidget(QWidget):
    def __init__(self, edgeSelectedSignal=None):
        super().__init__()
        
        self.seed = randint(0, 1000)
        self.graph = None
        self.threshold = 1.0
        self.labels = None
        self.clusters = None
        self.setMouseTracking(True)
        self.highlighted_edge = None
        self.clicked_edge = None
        self.edgeSelectedSignal = edgeSelectedSignal
        
    def setup(self, distance_matrix, threshold, clusters=[], labels=[], used_clusters=[]):
        n = len(distance_matrix)
        if labels and len(labels) != n:
            raise ValueError("Number of labels must match number of nodes")
        if clusters and len(clusters) != n:
            raise ValueError("Each node must have a cluster assignment")
        self.distance_matrix = distance_matrix
        self.graph = nx.Graph()
        self.labels = labels
        self.clusters = clusters
        self.used_clusters = used_clusters
        for i in range(n):
            if clusters and not clusters[i] in used_clusters:
                continue
            for j in range(i + 1, n):
                if clusters and not clusters[j] in used_clusters:
                    continue
                if distance_matrix[i][j] <= threshold:
                    self.graph.add_edge(i, j, weight=distance_matrix[i][j], one_minus_weight=1 - distance_matrix[i][j])
        
        self.pos = nx.spring_layout(self.graph, seed=self.seed, weight='one_minus_weight', k=1.6)
        self._normalize()
        self.update()

    
    def update_filter(self, threshold=None, used_clusters=None):
        if threshold:
            self.threshold = threshold
        if used_clusters is not None:
            self.used_clusters = used_clusters
        self.setup(self.distance_matrix, self.threshold, self.clusters, self.labels, self.used_clusters)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        widget_area = QRectF(0, 0, self.width(), self.height())
        painter.fillRect(widget_area, QColor(255, 255, 255))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(widget_area)
        
        if not self.graph or self.graph.number_of_nodes() < 2:
            painter.drawText(widget_area, Qt.AlignCenter, "No data")
            painter.end()
            return
        
        margin = 20
        draw_area = QRectF(margin, margin, self.width() - 2*margin, self.height() - 2*margin)
        
        for e in self.graph.edges():
            start = QPointF(self.pos[e[0]][0] * draw_area.width() + draw_area.left(),
                            self.pos[e[0]][1] * draw_area.height() + draw_area.top())
            end = QPointF(self.pos[e[1]][0] * draw_area.width() + draw_area.left(),
                          self.pos[e[1]][1] * draw_area.height() + draw_area.top())
            
            if e == self.clicked_edge:
                painter.setPen(QPen(Qt.blue, 4))
            elif e == self.highlighted_edge:
                painter.setPen(QPen(Qt.green, 3))
            else:
                # normally the weight would be within the range [0, self.threshold]
                # weight = self.graph[e[0]][e[1]]['weight']
                # from 0 to 0.5 red -> yellow, from 0.5 to 1 yellow -> green
                weight = self.graph[e[0]][e[1]]['weight']
                if weight < 0.5:
                    color = QColor.fromRgbF(1, 2*weight, 0)
                else:
                    color = QColor.fromRgbF(2-2*weight, 1, 0)
                painter.setPen(QPen(color, 2))
            painter.drawLine(start, end)
            
        for v in self.graph.nodes():
            x = self.pos[v][0] * draw_area.width() + draw_area.left()
            y = self.pos[v][1] * draw_area.height() + draw_area.top()
            color = QColor.fromRgb(0x66CCFF)
            if self.clusters:
                color = CLUSTER_COLORS[self.clusters[v] % len(CLUSTER_COLORS)]
            painter.setBrush(color)
            painter.setPen(QPen(Qt.black))
            painter.drawEllipse(QPointF(x, y), 6, 6)

            if self.labels:
                painter.drawText(int(x + 10), int(y + 5), str(self.labels[v]))
                
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_edge = self._get_edge_at(event.pos())
            if clicked_edge and self.edgeSelectedSignal and clicked_edge == self.clicked_edge:
                self.edgeSelectedSignal.emit((clicked_edge[0], clicked_edge[1]))
                self.clicked_edge = None
            else:
                self.clicked_edge = clicked_edge
            self.update()
            
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.highlighted_edge = self._get_edge_at(a0.pos())
        self.update()
    
    def _normalize(self):
        all_xs = [pos[0] for pos in self.pos.values()]
        all_ys = [pos[1] for pos in self.pos.values()]
        if len(all_xs) < 2 or len(all_ys) < 2:
            return
        min_x, max_x = min(all_xs), max(all_xs)
        min_y, max_y = min(all_ys), max(all_ys)
        for node, pos in self.pos.items():
            nx = (pos[0] - min_x) / (max_x - min_x) if max_x != min_x else 0.5
            ny = (pos[1] - min_y) / (max_y - min_y) if max_y != min_y else 0.5
            self.pos[node] = (nx, ny)   
    
    def _get_edge_at(self, pos):
        if not self.graph:
            return None
        margin = 20
        draw_area = QRectF(margin, margin, self.width() - 2*margin, self.height() - 2*margin)
        triggerd_edges = []
        for e in self.graph.edges():
            start = QPointF(self.pos[e[0]][0] * draw_area.width() + draw_area.left(),
                            self.pos[e[0]][1] * draw_area.height() + draw_area.top())
            end = QPointF(self.pos[e[1]][0] * draw_area.width() + draw_area.left(),
                          self.pos[e[1]][1] * draw_area.height() + draw_area.top())
            if _pointer_line_distance(pos, start, end) <= 5:
                triggerd_edges.append(e)
        if len(triggerd_edges) > 0:
            return triggerd_edges[0]
        return None
             
class EdgeSelectedSignal(QObject):
    edgeClicked = pyqtSignal(tuple)
    
    def emit(self, edge):
        self.edgeClicked.emit(edge)
        
    def connect(self, callback):
        self.edgeClicked.connect(callback)
               
def _pointer_line_distance(p, start, end, tolerance=5):
    x0, y0 = p.x(), p.y()
    x1, y1 = start.x(), start.y()
    x2, y2 = end.x(), end.y()
    
    # make a perpendicular line from the point to the line, and the line is beyond the start and end points
    if not min(x1, x2) - tolerance <= x0 <= max(x1, x2) + tolerance or \
      not min(y1, y2) - tolerance <= y0 <= max(y1, y2) + tolerance:
          return tolerance + 1
    return abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / ((y2-y1)**2 + (x2-x1)**2)**0.5
    
