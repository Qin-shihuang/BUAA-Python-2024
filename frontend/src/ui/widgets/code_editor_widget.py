import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPainter, QColor, QTextFormat, QFont, QTextCursor, QPalette
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt, QRect, QSize

from controllers.python_syntax_highlighter import PythonSyntaxHightlighter


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.display_line_numbers = True
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
        
        self.bg_highlight_manager = BackgroundHighlightManager(self)
        
    def set_text(self, text):
        self.setPlainText(text)
    
    def set_editable(self, editable):
        self.setReadOnly(not editable)
        
    def set_highlight(self, areas):
        self.bg_highlight_manager.set_highlight_areas(areas)
        
    def clear_highlight(self):
        self.bg_highlight_manager.clear_highlight_areas()
        
    def set_top_highlight(self, area):
        self.bg_highlight_manager.set_top_highlight_area(area)
        
    def get_top_highlight(self):
        return self.bg_highlight_manager.top_highlight
        
    def clear_top_highlight(self):
        self.bg_highlight_manager.clear_top_highlight_area()

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
        if not self.display_line_numbers:
            return 0
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
        if not self.display_line_numbers:
            return
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

class BackgroundHighlightManager:
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
        self.top_highlight = None
        self.top_highlight_color = QColor(255, 100, 100, 100)
       
    def set_highlight_areas(self, areas):
        self.highlights = areas
        self.paint_highlight_areas()
    
    def add_highlight_area(self, area):
        self.highlights.append(area)
        self.paint_highlight_areas()
       
    def set_top_highlight_area(self, area):
        self.top_highlight = area
        self.paint_highlight_areas()
       
    def clear_highlight_areas(self):
        self.highlights = []
        self.editor.setExtraSelections(self.editor.extraSelections()[0:1])
       
    def clear_top_highlight_area(self):
        if self.top_highlight:
            self.top_highlight = None
            self.editor.setExtraSelections(self.editor.extraSelections()[0:-1])
        
    def paint_highlight_areas(self):
        extra_selections = self.editor.extraSelections()[0:1]
        
        for i, area in enumerate(self.highlights):
            selections = self.create_highlight_selection(area, self.colors[i % len(self.colors)])
            extra_selections.extend(selections)
        
        if self.top_highlight:
            top_selection = self.create_highlight_selection(self.top_highlight, self.top_highlight_color)
            extra_selections.extend(top_selection)
        
        self.editor.setExtraSelections(extra_selections)
           
    def create_highlight_selection(self, area, color):
        start_line, end_line = area
        if start_line < 1 or end_line <= start_line:
            return None

        selections = []

        for i in range(start_line - 1, end_line - 1):        
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            block = self.editor.document().findBlockByNumber(i)
            selection.cursor = QTextCursor(block)
            selections.append(selection)

        return selections