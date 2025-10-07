import requests
import os
from typing import Optional

class YandexDiskManager:
    def __init__(self, token: str):
        """
        Инициализация менеджера Yandex.Disk.

        Args:
            token (str): OAuth-токен Yandex.Disk.
        """
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"

    def upload_file(self, file_path: str, disk_path: str) -> bool:
        """
        Загружает файл на Yandex.Disk.

        Args:
            file_path (str): Локальный путь к файлу.
            disk_path (str): Путь для сохранения файла на Yandex.Disk.

        Returns:
            bool: Успешность загрузки.
        """
        headers = {"Authorization": f"OAuth {self.token}"}
        upload_url = f"{self.base_url}/upload?path={disk_path}&overwrite=true"
        response = requests.get(upload_url, headers=headers)
        if response.status_code != 200:
            return False

        href = response.json().get("href")
        with open(file_path, "rb") as file:
            upload_response = requests.put(href, files={"file": file})
        return upload_response.status_code == 201

    def download_file(self, disk_path: str, destination_path: str) -> bool:
        """
        Скачивает файл с Yandex.Disk.

        Args:
            disk_path (str): Путь к файлу на Yandex.Disk.
            destination_path (str): Локальный путь для сохранения файла.

        Returns:
            bool: Успешность скачивания.
        """
        headers = {"Authorization": f"OAuth {self.token}"}
        download_url = f"{self.base_url}/download?path={disk_path}"
        response = requests.get(download_url, headers=headers)
        if response.status_code != 200:
            return False

        download_link = response.json().get("href")
        download_response = requests.get(download_link)
        with open(destination_path, "wb") as file:
            file.write(download_response.content)
        return True

    def list_files(self, disk_path: str = "/") -> list:
        """
        Возвращает список файлов в указанной директории.

        Args:
            disk_path (str): Путь к директории на Yandex.Disk.

        Returns:
            list: Список файлов.
        """
        headers = {"Authorization": f"OAuth {self.token}"}
        response = requests.get(f"{self.base_url}?path={disk_path}", headers=headers)
        if response.status_code != 200:
            return []
        return response.json().get("_embedded", {}).get("items", [])
