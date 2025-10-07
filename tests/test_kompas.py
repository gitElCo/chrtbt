import win32com.client

try:
    kompas = win32com.client.Dispatch("KOMPAS.Application.23")  # Измените версию
    print("Успешное подключение к KOMPAS!")
    print(f"Версия KOMPAS: {kompas.Version}")
except Exception as e:
    print(f"Ошибка подключения к KOMPAS: {e}")
