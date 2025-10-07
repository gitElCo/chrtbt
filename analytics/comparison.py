from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis

class ComparisonChart:
    @staticmethod
    def compare_analyses(analyses: list, parameter: str) -> QChartView:
        chart = QChart()
        chart.setTitle(f"Сравнение по параметру: {parameter}")
        chart.setAnimationOptions(QChart.AllAnimations)

        series = QLineSeries()
        series.setName(parameter)

        for i, analysis in enumerate(analyses):
            value = analysis[parameter]
            series.append(i, value)

        chart.addSeries(series)

        axis_x = QCategoryAxis()
        for i in range(len(analyses)):
            axis_x.append(f"Чертёж {i+1}", i)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText(parameter)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view
