from PySide6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
                              QPushButton, QFileDialog, QMessageBox, QFrame, QHBoxLayout)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from ui.styles import Styles
from kompas_lib.analyzer import analyze_drawing
from kompas_lib.kompas_api import KompasAPI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Чертобот")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(Styles.LIGHT_THEME)
        self.setAcceptDrops(True)

        self.kompas_api = KompasAPI()
        if not self.kompas_api.is_initialized():
            QMessageBox.critical(self, "Ошибка", "Не удалось инициализировать KOMPAS API")
            self.close()
            return

        self.tab_widget = QTabWidget()
        self.setup_tabs()

        self.setCentralWidget(self.tab_widget)

    def setup_tabs(self):
        # Вкладка анализа чертежей
        self.analyze_tab = QWidget()
        self.setup_analyze_tab()

        # Вкладка экспорта в PDF
        self.export_pdf_tab = QWidget()
        self.setup_export_pdf_tab()

        # Вкладка экспорта в STEP
        self.export_step_tab = QWidget()
        self.setup_export_step_tab()

        # Вкладка настроек
        self.settings_tab = QWidget()
        self.setup_settings_tab()

        self.tab_widget.addTab(self.analyze_tab, "Анализ чертежей")
        self.tab_widget.addTab(self.export_pdf_tab, "Экспорт в PDF")
        self.tab_widget.addTab(self.export_step_tab, "Экспорт в STEP")
        self.tab_widget.addTab(self.settings_tab, "Настройки")

    def setup_analyze_tab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Анализ чертежей")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        self.drop_area = QFrame()
        self.drop_area.setObjectName("drop_area")
        self.drop_area.setFixedHeight(200)

        drop_layout = QVBoxLayout()
        drop_label = QLabel("Перетащите файлы с чертежами сюда")
        drop_label.setAlignment(Qt.AlignCenter)
        drop_label.setStyleSheet("font-size: 14px;")
        drop_layout.addWidget(drop_label)
        self.drop_area.setLayout(drop_layout)

        layout.addWidget(self.drop_area)

        analyze_button = QPushButton("Выбрать файл для анализа")
        analyze_button.clicked.connect(self.analyze_file)
        layout.addWidget(analyze_button)

        self.analyze_tab.setLayout(layout)

    def setup_export_pdf_tab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Экспорт в PDF")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        export_button = QPushButton("Выбрать файл для экспорта в PDF")
        export_button.clicked.connect(self.export_to_pdf)
        layout.addWidget(export_button)

        self.export_pdf_tab.setLayout(layout)

    def setup_export_step_tab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Экспорт в STEP")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        export_button = QPushButton("Выбрать файл для экспорта в STEP")
        export_button.clicked.connect(self.export_to_step)
        layout.addWidget(export_button)

        self.export_step_tab.setLayout(layout)

    def setup_settings_tab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Настройки")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        theme_button = QPushButton("Переключить тему")
        theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_button)

        self.settings_tab.setLayout(layout)

    def analyze_file(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы для анализа", "", "KOMPAS Files (*.cdw)")
        if file_paths:
            self.process_files(file_paths)

    def process_files(self, file_paths):
        results = []
        for file_path in file_paths:
            result = analyze_drawing(file_path)
            if result:
                results.append(result)

        if results:
            QMessageBox.information(self, "Успех", f"Проанализировано {len(results)} файлов!")
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось проанализировать файлы!")

    def export_to_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для экспорта в PDF", "", "KOMPAS Files (*.cdw)")
        if file_path:
            QMessageBox.information(self, "Успех", f"Файл {file_path} будет экспортирован в PDF")

    def export_to_step(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для экспорта в STEP", "", "KOMPAS Files (*.m3d)")
        if file_path:
            QMessageBox.information(self, "Успех", f"Файл {file_path} будет экспортирован в STEP")

    def toggle_theme(self):
        if self.styleSheet() == Styles.LIGHT_THEME:
            self.setStyleSheet(Styles.DARK_THEME)
        else:
            self.setStyleSheet(Styles.LIGHT_THEME)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.process_files(file_paths)
