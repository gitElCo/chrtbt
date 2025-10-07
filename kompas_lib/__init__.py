from functools import lru_cache
from win32com.client import gencache
import pythoncom
import logging

logging.basicConfig(
    filename="chrtbt.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@lru_cache(maxsize=1)
def get_kompas_application():
    """
    Возвращает объект приложения KOMPAS.
    """
    pythoncom.CoInitialize()
    try:
        # Проверьте версию KOMPAS (22, 23, 24 и т.д.)
        kompas = gencache.EnsureDispatch("KOMPAS.Application.23")  # Измените на свою версию
        if kompas:
            logging.info("Успешное подключение к KOMPAS")
            return kompas
        else:
            logging.error("Не удалось подключиться к KOMPAS: объект не создан")
            return None
    except Exception as e:
        logging.error(f"Ошибка подключения к KOMPAS: {e}")
        return None
