from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton, QListWidget
from analytics.visualization import DataVisualizer
from analytics.comparison import ComparisonChart

class AdvancedAnalytics(QWidget):
    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        self.visualizer = DataVisualizer()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Фильтры
        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Листы", "Таблицы", "Размеры", "Сборки"])
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Поиск...")
        self.apply_button = QPushButton("Применить")
        self.apply_button.clicked.connect(self.apply_filters)

        filter_layout.addWidget(QLabel("Фильтр:"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.search_line)
        filter_layout.addWidget(self.apply_button)

        # Графики
        self.chart_view = self.visualizer.create_bar_chart(self.data)

        layout.addLayout(filter_layout)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def apply_filters(self):
        """Применяет фильтры."""
        filter_type = self.filter_combo.currentText()
        search_text = self.search_line.text().lower()

        if filter_type == "Листы":
            filtered_data = [sheet for sheet in self.data["sheets"] if search_text in sheet["name"].lower()]
            self.chart_view.setChart(self.visualizer.create_bar_chart({"sheets": filtered_data}).chart())

    def compare_analyses(self):
        """Сравнивает анализы нескольких чертежей."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout
        dialog = QDialog(self)
        dialog.setWindowTitle("Сравнение анализов")
        dialog.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        parameter_combo = QComboBox()
        parameter_combo.addItems(["sheets", "dimensions", "tech_requirements", "assembly_parts"])

        # Пример данных для сравнения
        analyses = [self.data, self.data]  # Замените на реальные данные
        chart_view = ComparisonChart.compare_analyses(analyses, parameter_combo.currentText())
        layout.addWidget(parameter_combo)
        layout.addWidget(chart_view)

        parameter_combo.currentTextChanged.connect(
            lambda param: layout.replaceWidget(chart_view, ComparisonChart.compare_analyses(analyses, param))
        )

        dialog.setLayout(layout)
        dialog.exec()
