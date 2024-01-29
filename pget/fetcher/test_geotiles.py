import unittest
from geotiles import ahn_subunit_indicies_of_city


class TestGeoTile(unittest.TestCase):
    def test_ahn(self) -> None:
        tiles = ahn_subunit_indicies_of_city("Delft")
        expected = [
            "37EZ1_03",
            "37EZ1_04",
            "37EZ1_05",
            "37EN1_04",
            "37EN1_05",
            "37EN1_08",
            "37EN1_09",
            "37EN1_10",
            "37EN1_12",
            "37EN1_13",
            "37EN1_14",
            "37EN1_15",
            "37EN1_17",
            "37EN1_18",
            "37EN1_19",
            "37EN1_20",
            "37EN1_23",
            "37EN1_24",
            "37EN1_25",
            "37EZ2_01",
            "37EZ2_02",
            "37EZ2_03",
            "37EZ2_08",
            "37EN2_01",
            "37EN2_02",
            "37EN2_06",
            "37EN2_07",
            "37EN2_11",
            "37EN2_12",
            "37EN2_16",
            "37EN2_17",
            "37EN2_21",
            "37EN2_22",
            "37EN2_23",
        ]
        self.assertEqual(tiles, expected)


if __name__ == "__main__":
    unittest.main()
