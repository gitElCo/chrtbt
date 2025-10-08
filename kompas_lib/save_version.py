from kompas_lib import iApplication, iDocuments, KompasConst, KompasAPI7
from PySide6.QtWidgets import QMessageBox
import os

def save_to_old_version():
    """
    Сохраняет текущий документ в старую версию KOMPAS.
    """
    if not iApplication.ActiveDocument:
        QMessageBox.critical(None, "Ошибка", "Нет активного документа в KOMPAS!")
        return

    # Запрашиваем версию для сохранения
    version = iApplication.ksReadString("Введите версию для сохранения (например, 19.0):", "19.0")
    if not version:
        return

    try:
        version_float = float(version)
    except ValueError:
        QMessageBox.critical(None, "Ошибка", "Введите числовое значение версии!")
        return

    # Определяем код версии для KOMPAS
    version_dict = {
        5.11: 1, 6.0: 2, 6.1: 3, 7.0: 4, 7.1: 5, 8.0: 6, 8.1: 7, 9.0: 8,
        10.0: 9, 11.0: 10, 12.0: 11, 13.0: 12, 14.0: 13, 14.1: 14, 14.2: 15,
        15.0: 16, 15.1: 17, 16.0: 19, 16.1: 20, 17.0: 21, 17.1: 22,
        18.0: 23, 18.1: 24, 19.0: 25, 20.0: 26, 21.0: 27, 22.0: 28, 23.0: 29
    }

    if version_float not in version_dict:
        QMessageBox.critical(None, "Ошибка", f"Версия {version} не поддерживается!")
        return

    save_mode = version_dict[version_float]

    # Запрашиваем путь для сохранения
    doc = iApplication.ActiveDocument
    file_path, _ = QFileDialog.getSaveFileName(None, "Сохранить как", "", "KOMPAS Files (*.cdw *.m3d)")
    if not file_path:
        return

    # Сохраняем документ
    doc.SaveAs(file_path, save_mode)
    QMessageBox.information(None, "Успех", f"Документ сохранён в версию {version}!")
