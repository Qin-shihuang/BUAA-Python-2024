import sys

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QMenu, QAction, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

from ui.widgets.code_editor_widget import CodeEditor

files = {
    "File 1": "def hello_world():\n"
                "    print('Hello World1!')\n",
    "File 2": "def hello_world():\n"
                "    print('Hello World!2')\n",
    "File 3": "def hello_world():\n"
                "    print('Hello World!3')\n",
}
class CodeComparingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Code Comparing - {1} vs {2}") 
        self.setGeometry(100, 100, 1920, 1080)

        # MARK: - Layout
        self.layout = QVBoxLayout()

        # menuBar = self.menuBar()
        # menuBar.setStyleSheet("background-color: white; color: black;")
        # fileMenu = menuBar.addMenu("File")
        # fileMenu.addAction("New")
        # menuBar.addSeparator()
        self.flag_button = QPushButton("Flag")
        self.flag_button.setEnabled(False)
        self.flag_button.clicked.connect(self.on_flag_button_clicked)
        self.layout.addWidget(self.flag_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.on_clear_button_clicked)
        self.layout.addWidget(self.clear_button)
        
        mainLayout = QHBoxLayout()
        self.layout.addLayout(mainLayout)

        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()
        self.leftFileSelectionDropdown = QComboBox()
        self.leftFileSelectionDropdown.setFixedHeight(25)
        self.rightFileSelectionDropdown = QComboBox()
        self.rightFileSelectionDropdown.setFixedHeight(25)
        self.leftCE = CodeEditor()
        self.rightCE = CodeEditor()
        leftLayout.addWidget(self.leftFileSelectionDropdown)
        leftLayout.addWidget(self.leftCE)
        rightLayout.addWidget(self.rightFileSelectionDropdown)
        rightLayout.addWidget(self.rightCE)
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setSpacing(0)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: white;")
        
        # TODO:
        self.leftFileSelectionDropdown.addItems(["File 1", "File 2", "File 3"])
        self.rightFileSelectionDropdown.addItems(["File 1", "File 2", "File 3"])
        
        # MARK: - Signals
        self.leftFileSelectionDropdown.currentIndexChanged.connect(self.left_file_changed)
        self.rightFileSelectionDropdown.currentIndexChanged.connect(self.right_file_changed)
        self.leftFileSelectionDropdown.currentIndexChanged.emit(0)
        self.rightFileSelectionDropdown.currentIndexChanged.emit(0)
        
        self.leftTextSelected = False
        self.rightTextSelected = False
        
        self.leftCE.selectionChanged.connect(self.on_left_selection_changed)
        self.rightCE.selectionChanged.connect(self.on_right_selection_changed)
        
    def left_file_changed(self, index):
        self.leftCE.setPlainText(files[self.leftFileSelectionDropdown.currentText()])
        
    def right_file_changed(self, index):
        self.rightCE.setPlainText(files[self.rightFileSelectionDropdown.currentText()])
        
    def on_left_selection_changed(self):
        cursor = self.leftCE.textCursor()
        if cursor.hasSelection() and not self.leftTextSelected:
            self.leftTextSelected = True
            if self.rightTextSelected:
                self.flag_button.setEnabled(True)
        elif not cursor.hasSelection() and self.leftTextSelected:
            self.leftTextSelected = False
            self.flag_button.setEnabled(False)
     

    def on_right_selection_changed(self):
        cursor = self.rightCE.textCursor()
        if cursor.hasSelection() and not self.rightTextSelected:
            self.rightTextSelected = True
            if self.leftTextSelected:
                self.flag_button.setEnabled(True)
        elif not cursor.hasSelection() and self.rightTextSelected:
            self.rightTextSelected = False
            self.flag_button.setEnabled(False)
            
    def on_flag_button_clicked(self):
        if not self.leftCE.textCursor().hasSelection() or not self.rightCE.textCursor().hasSelection():
            return
        lcursor = self.leftCE.textCursor()
        rcursor = self.rightCE.textCursor()
        lpos = get_pos_from_cursor(lcursor)
        rpos = get_pos_from_cursor(rcursor)
        self.leftCE.add_hightlight_areas([lpos])
        self.rightCE.add_hightlight_areas([rpos])
        lcursor.setPosition(lcursor.selectionStart(), QTextCursor.MoveAnchor)
        rcursor.setPosition(rcursor.selectionStart(), QTextCursor.MoveAnchor)
        self.leftCE.setTextCursor(lcursor)
        self.rightCE.setTextCursor(rcursor)
        
    def on_clear_button_clicked(self):
        self.leftCE.clear_highlight()
        self.rightCE.clear_highlight()

def get_pos_from_cursor(cursor):
    start = cursor.selectionStart()
    end = cursor.selectionEnd()
    
    start_cursor = QTextCursor(cursor.document())
    start_cursor.setPosition(start)
    start_line = start_cursor.blockNumber() + 1
    start_col = start - start_cursor.block().position() + 1
    
    end_cursor = QTextCursor(cursor.document())
    end_cursor.setPosition(end)
    end_line = end_cursor.blockNumber() + 1
    end_col = end - end_cursor.block().position() + 1
    
    return start_line, start_col, end_line, end_col
    
    
        
    


