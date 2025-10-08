from win32com.client import Dispatch, gencache
from pywintypes import com_error as COMError
import logging

class KompasAPI:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KompasAPI, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            # Импортируем необходимые модули из tlb-файлов
            self.kompas6_constants = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
            self.kompas6_constants_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants
            self.kompas6_api5_module = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
            self.kompas_api7_module = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)

            # Инициализация приложения KOMPAS
            self.iApplication = Dispatch("Kompas.Application.7")
            if not self.iApplication:
                raise RuntimeError("Не удалось инициализировать KOMPAS Application")

            self.iDocuments = self.iApplication.Documents
            self.initialized = True
        except COMError as e:
            logging.error(f"Ошибка инициализации KOMPAS API: {e}")
            self.initialized = False
        except Exception as e:
            logging.error(f"Неожиданная ошибка инициализации KOMPAS API: {e}")
            self.initialized = False

    def is_initialized(self):
        return self.initialized

    def open_document(self, file_path):
        if not self.is_initialized():
            raise RuntimeError("KOMPAS API не инициализирован")
        try:
            return self.iDocuments.Open(file_path, False, False)
        except COMError as e:
            logging.error(f"Ошибка открытия документа {file_path}: {e}")
            return None
        except Exception as e:
            logging.error(f"Неожиданная ошибка открытия документа {file_path}: {e}")
            return None
