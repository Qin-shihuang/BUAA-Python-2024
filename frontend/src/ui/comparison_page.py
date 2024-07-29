from PyQt5.QtWidgets import (QVBoxLayout, QToolBar, QAction, QWidget, 
                             QSplitter, QToolButton, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

from controllers.comparison_page_controller import ComparisonPageController
from ui.widgets.code_editor_widget import CodeEditor

class ComparisonPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.controller = ComparisonPageController()
        
        self.leftTextSelected = False
        self.rightTextSelected = False
        self.left_highlight_areas = []
        self.right_highlight_areas = []
        
        self.setGeometry(100, 100, 1920, 1080)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
    
        comparison_widget = QWidget()
        
        main_layout.addWidget(comparison_widget)
        comparison_layout = QVBoxLayout(comparison_widget)

        toolbar = QToolBar()
        comparison_layout.addWidget(toolbar)

        self.show_action = toolbar.addAction("Show")
        self.show_action.setCheckable(True)
        self.flag_action = toolbar.addAction("Flag") 
        self.clear_action = toolbar.addAction("Clear")
        self.submit_action = toolbar.addAction("Submit")

        toolbar.addSeparator()

        view_button = QToolButton()
        view_button.setText("View")
        view_menu = QMenu()
        sync_action = view_menu.addAction("Sync Scroll")
        sync_action.setCheckable(True)
        line_number_action = view_menu.addAction("Toggle Line Numbers")
        line_number_action.setCheckable(True)
        line_number_action.setChecked(True)
        view_button.setMenu(view_menu)
        view_button.setPopupMode(QToolButton.InstantPopup)
        toolbar.addWidget(view_button)

        splitter = QSplitter(Qt.Horizontal)
        comparison_layout.addWidget(splitter)

        self.leftCE = CodeEditor()
        self.rightCE = CodeEditor()
        self.leftCE.set_editable(False)
        self.rightCE.set_editable(False)
        splitter.addWidget(self.leftCE)
        splitter.addWidget(self.rightCE)

        self.setLayout(main_layout)
        
        self.leftCE.selectionChanged.connect(self._on_left_selection_changed)
        self.rightCE.selectionChanged.connect(self._on_right_selection_changed)
        
        sync_action.triggered.connect(self._on_sync_changed)
        line_number_action.triggered.connect(self._on_line_number_changed)
        self.show_action.triggered.connect(self._on_show_changed)
        self.flag_action.triggered.connect(self._on_flag_button_clicked)
        self.clear_action.triggered.connect(self._on_clear_button_clicked)
        self.submit_action.triggered.connect(self._on_submit_button_clicked)   
        
    def setup(self, reportId):
        self.controller.set_report(reportId)
        
        self.setWindowTitle("Comparison: {} vs {}".format(self.controller.file1_name, self.controller.file2_name))
        self.leftCE.set_text(self.controller.left_content)
        self.rightCE.set_text(self.controller.right_content)
        
        self.left_highlight_areas = self.controller.left_highlight_areas
        self.right_highlight_areas = self.controller.right_highlight_areas
        
    def _on_show_changed(self, enable):
        if enable:
            self.leftCE.set_highlight(self.left_highlight_areas)
            self.rightCE.set_highlight(self.right_highlight_areas)
        else:
            self.leftCE.clear_highlight()
            self.rightCE.clear_highlight()
            
    def _on_line_number_changed(self, enable):
        self.leftCE.display_line_numbers = enable
        self.rightCE.display_line_numbers = enable
        self.leftCE.update_line_number_area_width()
        self.rightCE.update_line_number_area_width()
        self.leftCE.update()
        self.rightCE.update()
        
    def _on_sync_changed(self, enable):
        if enable:
            self.leftCE.verticalScrollBar().valueChanged.connect(self.rightCE.verticalScrollBar().setValue)
            self.rightCE.verticalScrollBar().valueChanged.connect(self.leftCE.verticalScrollBar().setValue)
        else:
            self.leftCE.verticalScrollBar().valueChanged.disconnect(self.rightCE.verticalScrollBar().setValue)
            self.rightCE.verticalScrollBar().valueChanged.disconnect(self.leftCE.verticalScrollBar().setValue)
                
    def _on_flag_button_clicked(self):
        if not self.leftCE.textCursor().hasSelection() or not self.rightCE.textCursor().hasSelection():
            return
        lcursor = self.leftCE.textCursor()
        rcursor = self.rightCE.textCursor()
        lpos = get_pos_from_cursor(lcursor)
        rpos = get_pos_from_cursor(rcursor)
        self.leftCE.set_top_highlight(lpos)
        self.rightCE.set_top_highlight(rpos)
        lcursor.setPosition(lcursor.selectionStart(), QTextCursor.MoveAnchor)
        rcursor.setPosition(rcursor.selectionStart(), QTextCursor.MoveAnchor)
        self.leftCE.setTextCursor(lcursor)
        self.rightCE.setTextCursor(rcursor)
        self.clear_action.setEnabled(True)
        self.submit_action.setEnabled(True)

    def _on_clear_button_clicked(self):
        self.leftCE.clear_top_highlight()
        self.rightCE.clear_top_highlight()
        self.clear_action.setEnabled(False)
        self.submit_action.setEnabled(False)

    def _on_submit_button_clicked(self):
        left_top = self.leftCE.get_top_highlight()
        right_top = self.rightCE.get_top_highlight()
        if left_top and right_top:
            self.left_highlight_areas.append(left_top)
            self.right_highlight_areas.append(right_top)
            self.leftCE.clear_top_highlight()
            self.rightCE.clear_top_highlight()
            if self.show_action.isChecked():
                self.leftCE.set_highlight(self.left_highlight_areas)
                self.rightCE.set_highlight(self.right_highlight_areas)
            self.controller.add_highlight_area((left_top, right_top))
            self.clear_action.setEnabled(False)
            self.submit_action.setEnabled(False)
    
    def _on_left_selection_changed(self):
        cursor = self.leftCE.textCursor()
        if cursor.hasSelection() and not self.leftTextSelected:
            self.leftTextSelected = True
            if self.rightTextSelected:
                self.flag_action.setEnabled(True)
        elif not cursor.hasSelection() and self.leftTextSelected:
            self.leftTextSelected = False
            self.flag_action.setEnabled(False)
        
    def _on_right_selection_changed(self):
        cursor = self.rightCE.textCursor()
        if cursor.hasSelection() and not self.rightTextSelected:
            self.rightTextSelected = True
            if self.leftTextSelected:
                self.flag_action.setEnabled(True)
        elif not cursor.hasSelection() and self.rightTextSelected:
            self.rightTextSelected = False
            self.flag_action.setEnabled(False)
            
def get_pos_from_cursor(cursor):
    start = cursor.selectionStart()
    end = cursor.selectionEnd()
    
    start_cursor = QTextCursor(cursor.document())
    start_cursor.setPosition(start)
    start_line = start_cursor.blockNumber() + 1
    
    end_cursor = QTextCursor(cursor.document())
    end_cursor.setPosition(end)
    end_line = end_cursor.blockNumber() + 2
    if end_cursor.block().position() == end:
        end_line -= 1
    
    return start_line, end_line
    
    