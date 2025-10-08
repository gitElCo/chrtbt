from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChartView, QBarSeries, QBarSet, QChart, QCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class AnalyticsTab(QWidget):
    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.chart_view = self.create_bar_chart(self.data)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def create_bar_chart(self, data: dict) -> QChartView:
        """Создает столбчатую диаграмму."""
        if not data or "sheets" not in data:
            data = {"sheets": [{"name": "No Data", "format": "N/A"}]}

        series = QBarSeries()
        bar_set = QBarSet("Значения")

        for sheet in data["sheets"]:
            bar_set.append(1)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Анализ чертежей")
        chart.setAnimationOptions(QChart.AllAnimations)

        axis_x = QCategoryAxis()
        axis_x.append("Листы", 0)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

    def update_data(self, data: dict):
        """Обновляет данные для аналитики."""
        self.data = data
        self.chart_view.setChart(self.create_bar_chart(self.data).chart())
