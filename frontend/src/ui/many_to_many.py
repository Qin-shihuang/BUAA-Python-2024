import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
import itertools
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox, QMenu, QAction, QMessageBox, QTabWidget, \
    QSplitter, QLayout, QScrollArea, QFrame
    
from widgets.graph_widget import GraphWidget, EdgeSelectedSignal, CLUSTER_COLORS
from widgets.filter_widget import FilterWidget, ThresholdChangedSignal
from widgets.dynamic_checkbox_widget import DynamicCheckboxWidget, CheckboxChangedSignal
    
class ManyToManyTaskWindow(QWidget):
    def __init__(self):
        super().__init__()

        # TODO: Add task name
        self.setWindowTitle("Many to Many Task")
        self.setFixedSize(854, 935)
                    
        layout = QVBoxLayout()
        tab_widget = QTabWidget()
        self.graph_tab = QWidget()
        self._init_graph_tab()
        self.table_widget = QTableWidget()
        
        tab_widget.setContentsMargins(0, 0, 0, 0)
        tab_widget.addTab(self.graph_tab, "Graph")
        tab_widget.addTab(self.table_widget, "Table")
        layout.addWidget(tab_widget)
        self.setLayout(layout)
        
    def _init_graph_tab(self):
        edge_selected_signal = EdgeSelectedSignal()
        threshold_changed_signal = ThresholdChangedSignal()
        cluster_selection_changed_signal = CheckboxChangedSignal()
        
        layout = QVBoxLayout()
        mid_layout = QHBoxLayout()
        mid_layout.setContentsMargins(10, 0, 0, 0)

        self.graph_widget = GraphWidget(edgeSelectedSignal=edge_selected_signal)
        self.graph_widget.setFixedSize(800, 600)        
        self.graph_widget.setStyleSheet("border: 10px solid black")

        self.filter_widget = FilterWidget(thresholdChangedSignal=threshold_changed_signal)
        self.filter_widget.setFixedSize(650, 100)
        self.graph_label = QLabel()
        
        self.cluster_select_area = DynamicCheckboxWidget(checkboxChangedSignal=cluster_selection_changed_signal)
        layout.addWidget(self.graph_widget)
        layout.addLayout(mid_layout)
        layout.addWidget(self.cluster_select_area)

        mid_layout.addWidget(self.filter_widget)
        mid_layout.addWidget(self.graph_label)
        mid_layout.setAlignment(self.filter_widget, Qt.AlignVCenter)
        
        self.graph_tab.setLayout(layout)
        

        edge_selected_signal.connect(self._on_edge_selected)
        threshold_changed_signal.connect(self._on_threshold_changed)
        cluster_selection_changed_signal.connect(self._on_cluster_selection_changed)
        
    
    def setup(self, taskId):
        # WIP test data
        self.distance_matrix = [[0.00, 0.11, 0.21, 0.31, 0.41, 0.51],
                                [0.11, 0.00, 0.12, 0.22, 0.32, 0.42],
                                [0.21, 0.12, 0.00, 0.13, 0.23, 0.33],
                                [0.31, 0.22, 0.13, 0.00, 0.14, 0.24],
                                [0.41, 0.32, 0.23, 0.14, 0.00, 0.15],
                                [0.51, 0.42, 0.33, 0.24, 0.15, 0.00]]
        self.clustering = [0, 1, 2, 3, 4, 5]
        self.labels = ["A", "B", "C", "D", "E", "F"]
        self.graph_widget.setup(self.distance_matrix, 0.25, self.clustering, self.labels)
        self.filter_widget.setup([(i, j, self.distance_matrix[i][j]) for i, j in itertools.combinations(range(len(self.distance_matrix)), 2)])
        clusters = {}
        for i, c in enumerate(self.clustering):
            if c not in clusters:
                clusters[c] = []
            clusters[c].append(i)
        self.cluster_select_area.setup(len(clusters), CLUSTER_COLORS)
        
    def _on_edge_selected(self, edge):
        print(edge)
    
    def _on_threshold_changed(self, threshold, count):
        self.graph_widget.update_filter(threshold=threshold)
        self.graph_label.setText(f"Threshold: {threshold: .2f}\n\nSelected Edge count: {count}")
        
        
    def _on_cluster_selection_changed(self, checked):
        self.graph_widget.update_filter(used_clusters=checked)
        selected_lines = []
        for i, c in enumerate(self.clustering):
            if c in checked:
                selected_lines.append(i)
        data = []
        for i in selected_lines:
            for j in selected_lines:
                if i < j:
                    data.append((i, j, self.distance_matrix[i][j]))
        self.filter_widget.update_data(data)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManyToManyTaskWindow()
    window.show()
    window.setup(0)
    sys.exit(app.exec_())