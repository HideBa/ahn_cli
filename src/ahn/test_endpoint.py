import os
import unittest

from constant import BASE_URL
from endpoint import get_tile_endpoint


class TestEndpoint(unittest.TestCase):  # Convert the function to a test class
    def test_get_tile_endpoint(self) -> None:
        # Test case 1: index = "tile1"
        index = "tile1"
        expected = os.path.join(BASE_URL + "/03a_DSM_0.5m/tile1.zip")
        self.assertEqual(get_tile_endpoint(index), expected)

        # Test case 2: index = "tile2"
        index = "tile2"
        expected = os.path.join(BASE_URL + "/03a_DSM_0.5m/tile2.zip")
        self.assertEqual(get_tile_endpoint(index), expected)


if __name__ == "__main__":
    unittest.main()
