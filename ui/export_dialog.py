from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel

class ExportDialog(QDialog):
    def __init__(self, chart_view):
        super().__init__()
        self.chart_view = chart_view
        self.setWindowTitle("Экспорт графика")
        self.setGeometry(300, 300, 400, 150)

        layout = QVBoxLayout()

        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "SVG"])

        self.export_button = QPushButton("Экспортировать")
        self.export_button.clicked.connect(self.export_chart)

        layout.addWidget(QLabel("Выберите формат:"))
        layout.addWidget(self.format_combo)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def export_chart(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить график",
            "",
            f"Images ({self.format_combo.currentText().lower()} *.{self.format_combo.currentText().lower()})"
        )
        if file_path:
            from analytics.visualization import export_chart_to_image
            export_chart_to_image(self.chart_view, file_path, self.format_combo.currentText())
            QMessageBox.information(self, "Успех", "График сохранён!")
