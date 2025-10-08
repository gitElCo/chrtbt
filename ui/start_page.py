from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from ui.main_window import MainWindow

class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Чертобот: Старт")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        title_label = QLabel("Добро пожаловать в Чертобот!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        analyze_button = QPushButton("Открыть Чертобот")
        analyze_button.setStyleSheet("padding: 10px; font-size: 14px;")
        analyze_button.clicked.connect(self.open_main_window)
        layout.addWidget(analyze_button)

        self.setLayout(layout)

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
