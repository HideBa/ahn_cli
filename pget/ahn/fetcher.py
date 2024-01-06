import os
import tempfile
from threading import Lock, Thread
import threading
from urllib.parse import urlparse
from .geotiles import ahn_subunit_indicies_of_city
import requests


class Fetcher:
    def __init__(self, base_url: str, city_name: str):
        if not self._check_valid_url(base_url):
            raise ValueError("Invalid URL")
        self.base_url = base_url
        self.city_name = city_name
        self.urls = self._construct_urls()

    def fetch(self) -> dict:
        def req(url: str, results: dict, lock: Lock) -> None:
            res = requests.get(url, stream=True)
            with tempfile.NamedTemporaryFile(
                delete=False, mode="w+b", suffix=".tmp"
            ) as temp_file:
                for chunk in res.iter_content(chunk_size=1024):
                    temp_file.write(chunk)
                with lock:
                    results[url] = temp_file.name

        results: dict = {}
        lock = threading.Lock()
        threads = []
        for url in self.urls:
            thread = Thread(target=req, args=(url, results, lock))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return results

    def _check_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except ValueError:
            return False

    def _construct_urls(self) -> list[str]:
        tiles_indices = ahn_subunit_indicies_of_city(self.city_name)
        urls = []
        for tile_index in tiles_indices:
            urls.append(os.path.join(self.base_url + f"{tile_index}.LAZ"))

        return urls
