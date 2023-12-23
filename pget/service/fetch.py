import os
import tempfile
from ahn.fetcher import Fetcher
from core.interface.fetcher import IFetcher


class Fetch:
    def __init__(self, base_url: str, city_name: str):
        self.base_url = base_url
        self.city_name = city_name

    def fetch(self) -> None:
        fetcher: IFetcher = Fetcher(self.base_url, self.city_name)
        data = fetcher.fetch()
        for d in data:
            with tempfile.NamedTemporaryFile(delete=True, mode="w+b") as temp_file:
                temp_file.write(d)
                temp_file.seek(0)
                name = temp_file.name
                print("File name: ", name)
                print("File size: ", os.path.getsize(name))
