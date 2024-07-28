import sys

sys.path.append("src")

from PyQt5.QtWidgets import QApplication

from ui.comparison_page import ComparisonPage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ComparisonPage()
    main_window.show()
    sys.exit(app.exec_())