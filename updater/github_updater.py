import requests
import json
import os
import zipfile
import shutil
from typing import Optional

class GitHubUpdater:
    def __init__(self, repo_owner: str, repo_name: str):
        """
        Инициализация апдейтера GitHub.

        Args:
            repo_owner (str): Владелец репозитория.
            repo_name (str): Название репозитория.
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    def check_for_updates(self, current_version: str) -> Optional[dict]:
        """
        Проверяет наличие обновлений.

        Args:
            current_version (str): Текущая версия приложения.

        Returns:
            Optional[dict]: Информация о последнем релизе или None, если обновления не требуются.
        """
        response = requests.get(self.api_url)
        if response.status_code != 200:
            return None

        latest_release = response.json()
        if latest_release["tag_name"] != current_version:
            return latest_release
        return None

    def download_update(self, release: dict, download_path: str) -> bool:
        """
        Скачивает обновление.

        Args:
            release (dict): Информация о релизе.
            download_path (str): Путь для сохранения архива с обновлением.

        Returns:
            bool: Успешность скачивания.
        """
        download_url = release["assets"][0]["browser_download_url"]
        response = requests.get(download_url, stream=True)
        if response.status_code != 200:
            return False

        with open(download_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True

    def install_update(self, zip_path: str, install_path: str) -> bool:
        """
        Устанавливает обновление.

        Args:
            zip_path (str): Путь к архиву с обновлением.
            install_path (str): Путь для установки обновления.

        Returns:
            bool: Успешность установки.
        """
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(install_path)
        return True
