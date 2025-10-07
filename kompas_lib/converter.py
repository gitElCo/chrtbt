import os
import logging
from win32com.client import COMError

def export_to_pdf(kompas, file_path: str, output_folder: str) -> bool:
    """
    Экспортирует чертеж в PDF.
    """
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return False

    try:
        doc = kompas.Documents.Open(file_path, False, False)
        if not doc:
            logging.error(f"Не удалось открыть документ: {file_path}")
            return False

        output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}.pdf")
        doc.ExportToPDF(output_path)
        doc.Close(False)
        return True

    except COMError as e:
        logging.error(f"Ошибка COM при экспорте в PDF {file_path}: {e}")
        return False
    except Exception as e:
        logging.error(f"Неожиданная ошибка при экспорте в PDF {file_path}: {e}")
        return False

def export_to_step(kompas, file_path: str, output_path: str) -> bool:
    """
    Экспортирует 3D-модель в STEP.
    """
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return False

    try:
        doc = kompas.Documents.Open(file_path, False, False)
        if not doc or not hasattr(doc, "Assembly"):
            logging.error(f"Документ не является 3D-моделью: {file_path}")
            return False

        doc.Assembly.SaveAsSTEP(output_path)
        doc.Close(False)
        return True

    except COMError as e:
        logging.error(f"Ошибка COM при экспорте в STEP {file_path}: {e}")
        return False
    except Exception as e:
        logging.error(f"Неожиданная ошибка при экспорте в STEP {file_path}: {e}")
        return False
