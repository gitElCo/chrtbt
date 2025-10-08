from win32com.client import gencache, Dispatch
import pythoncom
import logging

# Глобальные переменные для констант и интерфейсов KOMPAS
KompasConst3D = None
KompasConst = None
KompasAPI5 = None
KompasAPI7 = None
iApplication = None
iDocuments = None

def init_kompas_api():
    """
    Инициализирует константы и интерфейсы KOMPAS.
    """
    global KompasConst3D, KompasConst, KompasAPI5, KompasAPI7, iApplication, iDocuments

    try:
        pythoncom.CoInitialize()

        # Подключение констант KOMPAS
        KompasConst3D = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants
        KompasConst = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
        KompasAPI5 = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
        KompasAPI7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)

        # Подключение к приложению KOMPAS
        iApplication = Dispatch("Kompas.Application.7")
        iApplication.Visible = True  # Делаем KOMPAS видимым
        iDocuments = iApplication.Documents

        logging.info("Успешное подключение к KOMPAS API")
        return True
    except Exception as e:
        logging.error(f"Ошибка инициализации KOMPAS API: {e}")
        return False
