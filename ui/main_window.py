from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog,
    QMessageBox, QMenu, QDialog, QComboBox, QCheckBox, QDoubleSpinBox, QTabWidget
)
from PySide6.QtGui import QFont, QIcon, QPixmap, QDragEnterEvent, QDropEvent, QShortcut, QKeySequence
from PySide6.QtCore import Qt
from ui.animations import fade_in, slide_in
from ui.styles import MacOSStyles
from ui.analytics_tab import AnalyticsTab
from ui.advanced_analytics import AdvancedAnalytics
from ui.export_dialog import ExportDialog
from kompas_lib.analyzer import analyze_drawing, analyze_3d_model
from kompas_lib.utils import process_files_multithreaded
from kompas_lib.watermark import add_watermark
from cloud.yandex_disk import YandexDiskManager
from updater.github_updater import GitHubUpdater
from plugins.plugin_manager import PluginManager
from kompas_lib import get_kompas_application
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Чертобот")
        self.setWindowIcon(QIcon("assets/icon.ico"))
        self.setGeometry(100, 100, 1200, 800)
        self.setAcceptDrops(True)
        self.set_style(MacOSStyles.LIGHT_THEME)


        # Проверка подключения к KOMPAS
        self.kompas = get_kompas_application()
        if not self.kompas:
            QMessageBox.critical(
                self,
                "Ошибка подключения",
                "Не удалось подключиться к KOMPAS-3D.\n"
                "1. Убедитесь, что KOMPAS-3D установлен.\n"
                "2. Запустите KOMPAS от имени администратора.\n"
                "3. Проверьте версию KOMPAS в коде (kompas_lib/__init__.py)."
            )
            self.close()  # Закрываем приложение, если KOMPAS недоступен
            return
        

        # Инициализация KOMPAS
        self.kompas = get_kompas_application()
        if not self.kompas:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к KOMPAS!")
            return

        # Инициализация менеджеров
        self.yandex_disk = YandexDiskManager("yandex_token")
        self.updater = GitHubUpdater("your_github_username", "chrtbt")
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

        # Данные для аналитики
        self.analysis_data = {
            "sheets": [{"name": "Sheet1", "format": "A3"}],
            "tech_requirements": 5,
            "tables": [{"rows": 3, "columns": 4}],
            "dimensions": 10,
            "developer_2d": "Иванов И.И.",
            "developer_3d": "Петров П.П.",
            "assembly_parts": 5,
            "executions": 2
        }

        # Виджеты
        self.title_label = QLabel("Чертобот")
        self.title_label.setFont(QFont("SF Pro Display", 24))

        self.analyze_button = QPushButton("Анализировать чертежи")
        self.analyze_button.setFont(QFont("SF Pro Text", 14))
        self.analyze_button.clicked.connect(self.open_files)

        self.export_pdf_button = QPushButton("Экспортировать в PDF с вотермаркой")
        self.export_pdf_button.setFont(QFont("SF Pro Text", 14))
        self.export_pdf_button.clicked.connect(self.export_to_pdf_with_watermark)

        # Вкладки
        self.tab_widget = QTabWidget()
        self.analytics_tab = AnalyticsTab(self.analysis_data)
        self.advanced_analytics = AdvancedAnalytics(self.analysis_data)
        self.tab_widget.addTab(self.analytics_tab, "Аналитика")
        self.tab_widget.addTab(self.advanced_analytics, "Расширенная аналитика")

        # Лэйаут
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.export_pdf_button)
        layout.addWidget(self.tab_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Меню
        self.setup_menus()

        # Горячие клавиши
        QShortcut(QKeySequence("Ctrl+O"), self, self.open_files)
        QShortcut(QKeySequence("Ctrl+S"), self, self.export_to_pdf_with_watermark)

        # Анимации
        fade_in(self.title_label)
        slide_in(self.analyze_button, direction="left")
        slide_in(self.export_pdf_button, direction="left")

        # Проверка обновлений
        self.check_for_updates()

    def setup_menus(self):
        """Настраивает меню приложения."""
        cloud_menu = self.menuBar().addMenu("Облако")
        yandex_action = QAction("Yandex.Disk", self)
        yandex_action.triggered.connect(self.upload_to_yandex_disk)
        cloud_menu.addAction(yandex_action)

        self.setup_plugin_menu()

        compare_menu = self.menuBar().addMenu("Сравнение")
        compare_action = QAction("Сравнить анализы", self)
        compare_action.triggered.connect(self.advanced_analytics.compare_analyses)
        compare_menu.addAction(compare_action)

    def setup_plugin_menu(self):
        """Настраивает меню плагинов."""
        plugin_menu = self.menuBar().addMenu("Плагины")
        for plugin_name in self.plugin_manager.plugins:
            action = QAction(plugin_name, self)
            action.triggered.connect(lambda _, name=plugin_name: self.run_plugin(name))
            plugin_menu.addAction(action)

    def set_style(self, style: str):
        """Устанавливает стиль приложения."""
        self.setStyleSheet(style)

    def open_files(self):
        """Открывает диалог выбора файлов."""
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "KOMPAS Files (*.cdw *.m3d)")
        if file_paths:
            self.process_files(file_paths)

    def process_files(self, file_paths: list):
        """Обрабатывает выбранные файлы."""
        results = process_files_multithreaded(
            file_paths,
            lambda path: analyze_drawing(self.kompas, path) if path.endswith(".cdw") else analyze_3d_model(self.kompas, path)
        )
        QMessageBox.information(self, "Успех", "Анализ завершён!")
        self.analysis_data = results[0]
        self.analytics_tab.update_data(self.analysis_data)
        self.advanced_analytics.update_data(self.analysis_data)

    def export_to_pdf_with_watermark(self):
        """Экспортирует чертеж в PDF с вотермаркой."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите чертеж", "", "KOMPAS Files (*.cdw)")
        if not file_path:
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF", "", "PDF Files (*.pdf)")
        if not output_path:
            return

        from kompas_lib.converter import export_to_pdf
        if not export_to_pdf(self.kompas, file_path, os.path.dirname(output_path)):
            QMessageBox.critical(self, "Ошибка", "Не удалось экспортировать в PDF.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Настройки вотермарки")
        dialog.setGeometry(300, 300, 400, 250)

        layout = QVBoxLayout()
        position_combo = QComboBox()
        position_combo.addItems(["center", "top-left", "top-right", "bottom-left", "bottom-right"])
        position_combo.setCurrentText("center")

        over_tech_check = QCheckBox("Разместить над техническими требованиями")
        scale_label = QLabel("Масштаб вотермарки:")
        scale_spin = QDoubleSpinBox()
        scale_spin.setRange(0.1, 5.0)
        scale_spin.setValue(1.0)
        scale_spin.setSingleStep(0.1)

        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(
            lambda: (
                add_watermark(
                    output_path,
                    output_path,
                    "assets/watermark.png",
                    position_combo.currentText(),
                    over_tech_check.isChecked(),
                    scale_spin.value()
                ),
                QMessageBox.information(self, "Успех", "Вотермарка добавлена!"),
                dialog.close()
            )
        )

        layout.addWidget(QLabel("Позиция вотермарки:"))
        layout.addWidget(position_combo)
        layout.addWidget(over_tech_check)
        layout.addWidget(scale_label)
        layout.addWidget(scale_spin)
        layout.addWidget(apply_button)

        dialog.setLayout(layout)
        dialog.exec()

    def upload_to_yandex_disk(self):
        """Загружает файл на Yandex.Disk."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для загрузки", "", "All Files (*)")
        if file_path:
            disk_path = f"/{os.path.basename(file_path)}"
            if self.yandex_disk.upload_file(file_path, disk_path):
                QMessageBox.information(self, "Успех", "Файл загружен на Yandex.Disk")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить файл")

    def check_for_updates(self):
        """Проверяет наличие обновлений."""
        current_version = "1.0.0"
        latest_release = self.updater.check_for_updates(current_version)
        if latest_release:
            reply = QMessageBox.question(
                self,
                "Обновление доступно",
                f"Доступна новая версия {latest_release['tag_name']}. Обновить?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.download_and_install_update(latest_release)

    def download_and_install_update(self, release: dict):
        """Скачивает и устанавливает обновление."""
        download_path = os.path.join(os.path.expanduser("~"), "chrtbt_update.zip")
        if self.updater.download_update(release, download_path):
            install_path = os.path.dirname(os.path.abspath(__file__))
            if self.updater.install_update(download_path, install_path):
                QMessageBox.information(self, "Успех", "Обновление установлено. Перезапустите приложение.")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось установить обновление.")
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось скачать обновление.")

    def run_plugin(self, plugin_name: str):
        """Запускает плагин."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if plugin:
            result = plugin.register()["analyze"]({"test": "data"})
            QMessageBox.information(self, "Результат плагина", str(result))

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Обработчик события перетаскивания файлов."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Обработчик события бросания файлов."""
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.process_files(file_paths)
