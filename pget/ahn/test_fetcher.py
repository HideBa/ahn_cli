import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
from threading import Thread
from .constant import BASE_URL
from .fetcher import Fetcher


class TestFetcher(unittest.TestCase):
    def test_fetch(self) -> None:
        fetcher = Fetcher(BASE_URL, "Westervoort")
        data = fetcher.fetch()

        print(len(data))


if __name__ == "__main__":
    import os
    import sys

    print("cwd-----", os.getcwd())
    sys.path.append(os.getcwd())
    unittest.main()
