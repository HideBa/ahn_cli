from urllib import request
from core.interface.fetcher import IFetcher


class Fecher(IFetcher):
    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> bytearray:
        content = request.urlopen(self.url).read()
        return content
