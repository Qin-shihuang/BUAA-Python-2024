import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
import itertools
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QCheckBox, QStackedWidget, QRadioButton, QListWidget, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QStyleOptionButton, QStyle, QComboBox, QMenu, QAction, QMessageBox, QTabWidget, \
    QSplitter, QLayout, QScrollArea, QFrame
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ClusterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: #e0e0e0;
                width: 10px;
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
        """)

        # self.resize(900, 600)
        self.setWindowTitle('Demo')

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['One', 'The other', 'Distance'])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.setFocusPolicy(Qt.NoFocus)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.cellDoubleClicked.connect(self.compare_for_table)

        cluster_widget = QWidget()
        cluster_layout = QVBoxLayout(cluster_widget)
        cluster_color = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black']
        cluster_num = self.get_cluster_num()

        self.graph = GraphVisualizer()

        for i in range(cluster_num):
            sub_widget = ClusterWidget(i, cluster_color[i], self.graph, self.table_widget)
            sub_widget.setObjectName(f'cluster{i}_widget')
            sub_widget.setStyleSheet(
                f'QWidget#cluster{i}_widget' + '{' + f'border:2px solid {cluster_color[i]};' + 'border-radius:15px;}')
            cluster_layout.addWidget(sub_widget)

        fig = self.graph.draw()
        canvas = FigureCanvas(fig)
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)
        graph_layout.addWidget(canvas)

        tab_widget = QTabWidget()
        tab_widget.addTab(graph_widget, 'Graph')
        tab_widget.addTab(self.table_widget, 'Table')

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(cluster_widget)
        scroll_area.setStyleSheet('QScrollArea { border: none; border-radius: 15px; }')

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(tab_widget)
        splitter.addWidget(scroll_area)

        # splitter.setSizes([1000, 900])
        splitter.setHandleWidth(10)
        layout = QVBoxLayout()

        layout.addWidget(splitter)
        self.setLayout(layout)

    def get_cluster_num(self):
        return 2
        # TODO: Implement this method

    def compare_for_table(self, row, col):
        cmp1 = self.table_widget.item(row, 0).text()
        cmp2 = self.table_widget.item(row, 1).text()
        print(cmp1, cmp2)
        # TODO: Implement this method


class ClusterWidget(QFrame):
    def __init__(self, cluster_no, cluster_color, graph, table_widget):
        super().__init__()
        i = cluster_no
        self.graph = graph
        self.table_widget = table_widget
        self.checked_boxes = 0
        self.checked_items = []
        sub_layout = QVBoxLayout(self)
        sub_label = QLabel(f'Cluster {i + 1}')
        sub_label.setFont(QFont("Arial", 11, QFont.Bold))
        sub_label.setStyleSheet(f'color:{cluster_color};')
        sub_label.setAlignment(Qt.AlignLeft)
        sub_layout.addWidget(sub_label)

        flow_layout = FlowLayout()

        elements = []
        for j in range(14):
            checkbox = QCheckBox(f'test{j}.py')
            checkbox.clicked.connect(self.limit_checkboxes)
            flow_layout.addWidget(checkbox)
            self.graph.addNode(f'test{i}{j}.py', f'{cluster_color}')
            elements.append(f'test{i}{j}.py')

        combinations = list(itertools.combinations(elements, 2))
        self.table_widget.setRowCount(len(combinations))
        for combo in combinations:
            self.graph.addEdge(combo[0], combo[1], 0.4)
            self.table_widget.setItem(combinations.index(combo), 0, QTableWidgetItem(combo[0]))
            self.table_widget.setItem(combinations.index(combo), 1, QTableWidgetItem(combo[1]))
            self.table_widget.setItem(combinations.index(combo), 2, QTableWidgetItem('0.4'))

        sub_layout.addLayout(flow_layout)

        sub_button_layout = QHBoxLayout()
        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red;')
        sub_button_layout.addWidget(self.error_label)
        sub_button_layout.addStretch(1)
        compare_button = QPushButton('Compare')
        sub_button_layout.addWidget(compare_button)
        compare_button.clicked.connect(self.start_compare)
        sub_layout.addLayout(sub_button_layout)

    def limit_checkboxes(self, state):
        sender = self.sender()
        if sender.isChecked():
            if self.checked_boxes >= 2:
                self.error_label.setText('You can only select 2 files to compare!')
                sender.setChecked(False)
            else:
                self.checked_items.append(sender.text())
                self.checked_boxes += 1
                self.error_label.setText('')
        else:
            self.checked_boxes -= 1
            self.checked_items.remove(sender.text())
            self.error_label.setText('')

    def start_compare(self):
        if self.checked_boxes != 2:
            QMessageBox.warning(self, 'Warning', 'Please select exactly 2 files to compare.', QMessageBox.Ok)
        else:
            print(self.checked_items[0], self.checked_items[1])
            self.error_label.setText('')
        # TODO: Implement this method


class GraphVisualizer:
    def __init__(self):
        self.graph = nx.Graph()
        self.color_map = []

    def addNode(self, name, color):
        self.graph.add_node(name)
        self.color_map.append(color)

    def addEdge(self, name1, name2, distance):
        self.graph.add_edge(name1, name2, weight=distance)

    def draw(self):
        pos = {}
        subgraphs = [self.graph.subgraph(c).copy() for c in nx.connected_components(self.graph)]
        offset = 0

        for i, subgraph in enumerate(subgraphs):
            subgraph_pos = nx.spring_layout(subgraph, seed=42, k=1)
            for key in subgraph_pos:
                subgraph_pos[key][0] += offset
            pos.update(subgraph_pos)
            offset += 2.3  # Adjust this value to control spacing between subgraphs

        fig, ax = plt.subplots(figsize=(12, 8))
        nx.draw(self.graph, pos, node_color=self.color_map, edge_color='black', node_size=300, font_size=10, ax=ax)

        # Draw labels manually to avoid overlapping with edges
        for node, (x, y) in pos.items():
            ax.text(x, y + 0.15, s=node, horizontalalignment='center', verticalalignment='center', fontsize=16,
                    bbox=dict(facecolor='white', alpha=0))

        ax.set_aspect('equal')  # Fix the aspect ratio
        return fig


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, hSpacing=10, vSpacing=10):
        super(FlowLayout, self).__init__(parent)
        self.itemList = []
        self.m_hSpace = hSpacing
        self.m_vSpace = vSpacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self.itemList.append(item)

    def horizontalSpacing(self):
        return self.m_hSpace

    def verticalSpacing(self):
        return self.m_vSpace

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.horizontalSpacing()
            spaceY = self.verticalSpacing()
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClusterWindow()
    window.show()
    sys.exit(app.exec_())
