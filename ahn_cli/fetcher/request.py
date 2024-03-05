import logging
import os
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from urllib.parse import urlparse

import requests
from tqdm import tqdm

from ahn_cli.fetcher.geotiles import (ahn_subunit_indicies_of_bbox,
                                      ahn_subunit_indicies_of_city)


class Fetcher:
    """
    Fetcher class for fetching AHN data.

    Args:
        base_url (str): The base URL for fetching AHN data.
        city_name (str): The name of the city for which to fetch AHN data.
        bbox (list[float] | None, optional): The bounding box coordinates [minx, miny, maxx, maxy]
            for a specific area of interest. Defaults to None.

    Raises:
        ValueError: If the base URL is invalid.

    Attributes:
        base_url (str): The base URL for fetching AHN data.
        city_name (str): The name of the city for which to fetch AHN data.
        bbox (list[float] | None): The bounding box coordinates [minx, miny, maxx, maxy]
            for a specific area of interest.
        urls (list[str]): The constructed URLs for fetching AHN data.

    Methods:
        fetch: Fetches AHN data.
        _check_valid_url: Checks if the base URL is valid.
        _construct_urls: Constructs the URLs for fetching AHN data.
    """

    def __init__(
        self, base_url: str, city_name: str, bbox: list[float] | None = None
    ):
        if not self._check_valid_url(base_url):
            raise ValueError("Invalid URL")
        self.base_url = base_url
        self.city_name = city_name
        self.bbox = bbox
        self.urls = self._construct_urls()

    def fetch(self) -> dict:
        """
        Fetches AHN data.

        Returns:
            dict: A dictionary containing the fetched AHN data, where the keys are the URLs
            and the values are the temporary file names where the data is stored.
        """
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
                    res.iter_content(chunk_size=500 * 1024 * 1024),
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
        """
        Checks if the base URL is valid.

        Args:
            url (str): The base URL to check.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except ValueError:
            return False

    def _construct_urls(self) -> list[str]:
        """
        Constructs the URLs for fetching AHN data.

        Returns:
            list[str]: A list of URLs for fetching AHN data.
        """
        tiles_indices = (
            ahn_subunit_indicies_of_bbox(self.bbox)
            if self.bbox
            else ahn_subunit_indicies_of_city(self.city_name)
        )
        urls = []
        for tile_index in tiles_indices:
            urls.append(os.path.join(self.base_url + f"{tile_index}.LAZ"))
        return urls
