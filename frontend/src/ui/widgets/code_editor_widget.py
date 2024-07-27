import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPainter, QColor, QTextFormat, QFont, QTextCursor, QPalette
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt, QRect, QSize

from controllers.python_syntax_highlighter import PythonSyntaxHightlighter


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setStyleSheet("font-size: 12pt; font-family: Consolas;")
        font = self.font()
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        palette = self.palette()
        palette.setColor(QPalette.Highlight, QColor(Qt.blue).lighter(180))
        palette.setColor(QPalette.HighlightedText, self.palette().color(QPalette.Text))
        self.setPalette(palette)        

        self.setTabStopDistance(QtGui.QFontMetricsF(self.font()).horizontalAdvance('_') * 4)
        self._highlighter = PythonSyntaxHightlighter(self.document())

        self.line_number_area = LineNumberWidget(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_focused_line)
        self.update_line_number_area_width()
        
        self.bg_highlight_manager = BackgroungHighlightManager(self)
        
    def set_text(self, text):
        self.setPlainText(text)
    
    def set_editable(self, editable):
        self.setReadOnly(not editable)
        
    def clear_highlight(self):
        self.bg_highlight_manager.clear_highlight_areas()
        
    def add_hightlight_areas(self, areas):
        for area in areas:
            self.bg_highlight_manager.add_highlight_area(area)

    # def set_font_size(self, size):
    #     font = self.font()
    #     font.setPointSize(size)
    #     self.setFont(font)
    
    # def increase_font_size(self):
    #     font = self.font()
    #     size = font.pointSize()
    #     print(size)
    #     self.set_font_size(size + 1)
    
    # def decrease_font_size(self):
    #     font = self.font()
    #     size = font.pointSize()
    #     if size > 1:
    #         self.set_font_size(size - 1)

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def update_line_number_area_width(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
        painter.end()

    def highlight_focused_line(self):
        cursor = self.textCursor()
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        highlight_color = QColor(Qt.lightGray).lighter(120)
        selections = self.extraSelections()
        if selections and selections[0].format.background().color() == highlight_color:
            selections = selections[1:]
        start_line = self.document().findBlock(selection_start).blockNumber()
        end_line = self.document().findBlock(selection_end).blockNumber()
        if start_line == end_line:
            current_line = self.document().findBlock(cursor.position())
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(highlight_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = QTextCursor(current_line)
            # line focus should be of the least priority
            selections = [selection] + selections
        self.setExtraSelections(selections)

class LineNumberWidget(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)
        
class BackgroungHighlightManager:
    def __init__(self, editor):
        self.editor = editor
        self.colors = [
            QColor(255, 255, 180),
            QColor(220, 255, 220),
            QColor(210, 230, 255),
            QColor(255, 220, 235),
            QColor(255, 225, 180),
            QColor(230, 220, 255),
            QColor(200, 255, 255),
            QColor(255, 220, 200),
            QColor(220, 240, 220),
            QColor(210, 240, 255),
        ]
        self.highlights = []
        
    def add_highlight_area(self, area):
        self.highlights.append(area)
        self.paint_highlight_area()
        
    def clear_highlight_areas(self):
        self.highlights = []
        self.editor.setExtraSelections(self.editor.extraSelections()[0:1])
        
    def paint_highlight_area(self):
        self.editor.setExtraSelections(self.editor.extraSelections()[0:1])
        for i, (start_row, start_col, end_row, end_col) in enumerate(self.highlights):
            if start_row < 1 or start_col < 1 or end_row < 1 or end_col < 1:
                continue
            if start_row > end_row or (start_row == end_row and start_col > end_col):
                continue
            if start_row == end_row and start_col == end_col:
                continue
            color = self.colors[i % len(self.colors)]   
            cursor = QTextCursor(self.editor.document())
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, start_row - 1)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start_col - 1)
            cursor.setPosition(cursor.position(), QTextCursor.KeepAnchor)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, end_row - start_row)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end_col - start_col)
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(color)
            selection.cursor = cursor
            self.editor.setExtraSelections(self.editor.extraSelections() + [selection])
            