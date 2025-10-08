from typing import Dict, List, Optional, Union
import logging
import os
from kompas_lib.kompas_api import KompasAPI

def analyze_drawing(file_path: str) -> Optional[Dict[str, Union[List, int, str]]]:
    """
    Анализирует чертеж KOMPAS и возвращает структурированные данные.
    """
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return None

    kompas_api = KompasAPI()
    if not kompas_api.is_initialized():
        logging.error("KOMPAS API не инициализирован")
        return None

    try:
        doc = kompas_api.open_document(file_path)
        if not doc:
            logging.error(f"Не удалось открыть документ: {file_path}")
            return None

        data = {
            "type": str(doc.Type),
            "sheets": [],
            "tech_requirements": 0,
            "tables": [],
            "dimensions": 0,
            "developer_2d": "",
            "developer_3d": "",
            "assembly_parts": 0,
            "executions": 0,
        }

        # Проверяем тип документа
        if doc.Type == kompas_api.kompas6_constants.ksDocumentDrawing:
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

        elif doc.Type == kompas_api.kompas6_constants.ksDocumentPart or doc.Type == kompas_api.kompas6_constants.ksDocumentAssembly:
            data["developer_3d"] = doc.Developer.Name

            if doc.Type == kompas_api.kompas6_constants.ksDocumentAssembly:
                data["assembly_parts"] = doc.Assembly.Parts.Count

        doc.Close(False)
        return data

    except Exception as e:
        logging.error(f"Ошибка при анализе {file_path}: {e}")
        return None
