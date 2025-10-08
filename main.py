import sys
from PySide6.QtWidgets import QApplication
from ui.start_page import StartPage

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_page = StartPage()
    start_page.show()
    sys.exit(app.exec())
