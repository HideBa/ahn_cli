import os
from queue import Queue
from threading import Thread
from urllib import request
from urllib.parse import urlparse
from .geotiles import ahn_subunit_indicies_of_city
from pget.core.interface.fetcher import IFetcher


class Fetcher(IFetcher):
    def __init__(self, base_url: str, city_name: str):
        if not self._check_valid_url(base_url):
            raise ValueError("Invalid URL")
        self.base_url = base_url
        self.city_name = city_name
        self.urls = self._construct_urls()

    def fetch(self) -> list[bytearray]:
        def req(url: str, queue: Queue) -> None:
            content = request.urlopen(url).read()
            queue.put(content)
            return

        data_queue: Queue = Queue()
        threads = []
        for url in self.urls:
            thread = Thread(target=req, args=(url, data_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        data = []
        while not data_queue.empty():
            data.append(data_queue.get())

        return data

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


# if __name__ == "__main__":
#     fetcher = Fetcher(BASE_URL, "Delft")
#     data = fetcher.fetch()
#     print(data)
