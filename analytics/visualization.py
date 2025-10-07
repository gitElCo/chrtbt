from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QPieSeries, QPieSlice,
    QLineSeries, QValueAxis, QCategoryAxis, QScatterSeries
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgGenerator

class DataVisualizer:
    @staticmethod
    def create_bar_chart(data: dict, title: str = "Анализ чертежей") -> QChartView:
        series = QBarSeries()
        bar_set = QBarSet("Значения")
        for sheet in data["sheets"]:
            bar_set.append(1)
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
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

    @staticmethod
    def export_chart_to_image(chart_view: QChartView, file_path: str, format: str = "PNG"):
        if format.upper() == "PNG":
            chart_view.grab().save(file_path, "PNG")
        elif format.upper() == "SVG":
            generator = QSvgGenerator()
            generator.setFileName(file_path)
            generator.setSize(chart_view.size())
            painter = QPainter(generator)
            chart_view.render(painter)
            painter.end()
