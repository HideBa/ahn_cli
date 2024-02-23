import logging
import os
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from urllib.parse import urlparse
from tqdm import tqdm

import requests

from ahn_cli.fetcher.geotiles import ahn_subunit_indicies_of_city


class Fetcher:
    def __init__(self, base_url: str, city_name: str):
        if not self._check_valid_url(base_url):
            raise ValueError("Invalid URL")
        self.base_url = base_url
        self.city_name = city_name
        self.urls = self._construct_urls()

    def fetch(self) -> dict:
        logging.info("Start fetching AHN data")
        logging.info(f"Fetching {len(self.urls)} tiles")

        def req(
            url: str, nth: int, results: dict, lock: Lock, pbar: tqdm
        ) -> None:
            res = requests.get(url, stream=True)
            with tempfile.NamedTemporaryFile(
                delete=False, mode="w+b", suffix=".laz"
            ) as temp_file:
                for chunk in tqdm(
                    res.iter_content(chunk_size=1024 * 1024),
                    desc="writing a file",
                ):
                    temp_file.write(chunk)
                with lock:
                    results[url] = temp_file.name
            pbar.update(1)

        results: dict = {}
        lock = threading.Lock()
        with tqdm(total=len(self.urls)) as pbar:
            pbar.set_description("Fetching AHN data")
            with ThreadPoolExecutor(max_workers=8) as executor:
                for i, url in enumerate(self.urls):
                    executor.submit(req, url, i, results, lock, pbar)
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
