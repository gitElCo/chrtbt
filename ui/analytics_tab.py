from PySide6.QtWidgets import QWidget, QVBoxLayout
from analytics.visualization import DataVisualizer

class AnalyticsTab(QWidget):
    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        self.visualizer = DataVisualizer()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.chart_view = self.visualizer.create_bar_chart(self.data)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def update_data(self, data: dict):
        """Обновляет данные для аналитики."""
        self.data = data
        self.chart_view.setChart(self.visualizer.create_bar_chart(self.data).chart())
