
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Any, List

def process_files_multithreaded(
    file_paths: List[str],
    func: Callable[[str], Any],
    max_workers: int = 4
) -> List[Any]:
    """
    Обрабатывает файлы в многопоточном режиме.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, path): path for path in file_paths}
        results = []
        for future in as_completed(futures):
            results.append(future.result())
        return results
