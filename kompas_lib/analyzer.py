from typing import Dict, List, Optional, Union
import logging
import os
from pywintypes import com_error as COMError

def analyze_drawing(kompas, file_path: str) -> Optional[Dict[str, Union[List, int, str]]]:
    """
    Анализирует чертеж KOMPAS и возвращает структурированные данные.
    Если у чертежа есть связанная 3D-модель, считывает её разработчика.
    """
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return None

    try:
        doc = kompas.Documents.Open(file_path, False, False)
        if not doc:
            logging.error(f"Не удалось открыть документ: {file_path}")
            return None

        data: Dict[str, Union[List, int, str]] = {
            "sheets": [],
            "tech_requirements": 0,
            "tables": [],
            "dimensions": 0,
            "developer_2d": "",
            "developer_3d": "",
            "assembly_parts": 0,
            "executions": 0,
        }

        sheets = doc.Sheets
        for sheet in sheets:
            data["sheets"].append({
                "name": sheet.Name,
                "format": sheet.Format,
            })

        tech_requirements = doc.TechRequirements
        data["tech_requirements"] = tech_requirements.Count

        tables = doc.Tables
        for table in tables:
            data["tables"].append({
                "rows": table.Rows.Count,
                "columns": table.Columns.Count,
            })

        dimensions = doc.Dimensions
        data["dimensions"] = dimensions.Count

        data["developer_2d"] = doc.Developer.Name

        if hasattr(doc, "Assembly"):
            data["developer_3d"] = doc.Assembly.Developer.Name
            data["assembly_parts"] = doc.Assembly.Parts.Count

        if hasattr(doc, "Executions"):
            data["executions"] = doc.Executions.Count

        doc.Close(False)
        return data

    except COMError as e:
        logging.error(f"Ошибка COM при анализе {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Неожиданная ошибка при анализе {file_path}: {e}")
        return None

def analyze_3d_model(kompas, file_path: str) -> Optional[Dict[str, Union[int, str, float]]]:
    """
    Анализирует 3D-модель KOMPAS.
    """
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return None

    try:
        doc = kompas.Documents.Open(file_path, False, False)
        if not doc or not hasattr(doc, "Assembly"):
            logging.error(f"Документ не является 3D-моделью: {file_path}")
            return None

        data = {
            "parts": doc.Assembly.Parts.Count,
            "developer": doc.Assembly.Developer.Name,
            "volume": doc.Assembly.Volume,
        }

        doc.Close(False)
        return data

    except COMError as e:
        logging.error(f"Ошибка COM при анализе 3D-модели {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Неожиданная ошибка при анализе 3D-модели {file_path}: {e}")
        return None
