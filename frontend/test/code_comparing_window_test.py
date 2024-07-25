import sys

sys.path.append("src")

from PyQt5.QtWidgets import QApplication

from ui.code_comparing_window import CodeComparingWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = CodeComparingWindow()
    main_window.show()
    sys.exit(app.exec_())