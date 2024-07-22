from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont

class PythonSyntaxHightlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.blue)
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                    'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
                    'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                    'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
                    'while', 'with', 'yield']
        for word in keywords:
            pattern = '\\b' + word + '\\b'
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)
            
        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(Qt.darkGreen)
        rule = ('#.*', single_line_comment_format)
        self.highlighting_rules.append(rule)
        
        single_quoted_string_format = QTextCharFormat()
        single_quoted_string_format.setForeground(Qt.darkGreen)
        rule = ("'.*'", single_quoted_string_format)
        self.highlighting_rules.append(rule)
        
        double_quoted_string_format = QTextCharFormat()
        double_quoted_string_format.setForeground(Qt.darkGreen)
        rule = ('".*"', double_quoted_string_format)
        self.highlighting_rules.append(rule)
        

    def highlightBlock(self, text):
        for pattern, highlighting_format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            index = expression.match(text)
            while index.hasMatch():
                length = index.capturedLength()
                self.setFormat(index.capturedStart(), length, highlighting_format)
                index = expression.match(text, index.capturedEnd())