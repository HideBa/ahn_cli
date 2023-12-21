import unittest
from ahn_tile import ahn_tile_indicies_of_city


class TestAHNTile(unittest.TestCase):
    def test_ahn_tile_indicies_of_city(self) -> None:
        tiles = ahn_tile_indicies_of_city("Delft")
        self.assertEqual(tiles, ["37EZ1", "37EN1", "37EZ2", "37EN2"])


if __name__ == "__main__":
    unittest.main()
