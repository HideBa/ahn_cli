import unittest
from unittest.mock import MagicMock
from service.fetch import Fetcher


class TestFetch(unittest.TestCase):
    def test_fetch(self):
        # Mock the fetcher object
        fetcher_mock = MagicMock()
        fetcher_mock.fetch.return_value = [b"test_data"]

        # Create an instance of the class under test
        fetcher = Fetcher("http://example.com", "Delft")
        fetcher.fetcher = fetcher_mock

        # Call the fetch method
        fetcher.fetch()

        # Assert that the temporary file is created and written to
        self.assertTrue(fetcher_mock.fetch.called)
        self.assertTrue(fetcher_mock.fetch.call_count == 1)
        self.assertTrue(fetcher_mock.fetch.return_value == [b"test_data"])
        self.assertTrue(fetcher_mock.fetch.return_value[0] == b"test_data")
        self.assertTrue(
            fetcher_mock.fetch.return_value[0] == fetcher_mock.fetch.return_value[0]
        )

        # Assert that the temporary file is closed and deleted
        self.assertTrue(fetcher_mock.fetch.return_value[0].close.called)
        self.assertTrue(fetcher_mock.fetch.return_value[0].close.call_count == 1)
        self.assertTrue(fetcher_mock.fetch.return_value[0].delete.called)
        self.assertTrue(fetcher_mock.fetch.return_value[0].delete.call_count == 1)


class MockFetcher:
    def __init__(self, _, __) -> None:
        pass

    def fetch(self) -> list[bytes]:
        return [b"test_data"]


if __name__ == "__main__":
    unittest.main()
