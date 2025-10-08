from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout, QSlider, QRadioButton, QButtonGroup
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import json
import os

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки Чертобота")
        self.setGeometry(100, 100, 500, 400)

        # Загружаем текущие настройки
        self.settings = self.load_settings()

        # Виджеты
        self.title_label = QLabel("Настройки")
        self.title_label.setFont(QFont("SF Pro Display", 20))

        self.check_update_box = QCheckBox("Проверять обновления")
        self.beta_box = QCheckBox("Скачивать бета-версии")
        self.model_name_box = QCheckBox("Брать обозначение из модели")
        self.rewrite_box = QCheckBox("Перезаписывать файлы")
        self.mass_saving_box = QCheckBox("Массовое сохранение")

        # Устанавливаем текущие значения
        self.check_update_box.setChecked(self.settings.get("check_update", False))
        self.beta_box.setChecked(self.settings.get("beta", False))
        self.model_name_box.setChecked(self.settings.get("model_name", False))
        self.rewrite_box.setChecked(self.settings.get("rewrite", False))
        self.mass_saving_box.setChecked(self.settings.get("mass_saving", False))

        # Кнопка сохранения
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_settings)

        # Лэйаут
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.check_update_box)
        layout.addWidget(self.beta_box)
        layout.addWidget(self.model_name_box)
        layout.addWidget(self.rewrite_box)
        layout.addWidget(self.mass_saving_box)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_settings(self):
        """Загружает настройки из файла."""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
        return {}

    def save_settings(self):
        """Сохраняет настройки в файл."""
        self.settings = {
            "check_update": self.check_update_box.isChecked(),
            "beta": self.beta_box.isChecked(),
            "model_name": self.model_name_box.isChecked(),
            "rewrite": self.rewrite_box.isChecked(),
            "mass_saving": self.mass_saving_box.isChecked(),
        }

        try:
            with open("settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)
            QMessageBox.information(self, "Успех", "Настройки сохранены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить настройки: {e}")
