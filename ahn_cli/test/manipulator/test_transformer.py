import unittest
from shapely.geometry import Polygon
from ahn_cli.manipulator.transformer import tranform_polygon


class TestTransformer(unittest.TestCase):
    def test_tranform_polygon(self) -> None:
        # Define the input polygon
        source_polygon = Polygon(  # EPSG:4326
            [
                [4.351433275357662, 52.003346279634385],
                [4.351433275359076, 52.029067702749337],
                [4.398517262087223, 52.029067702749764],
                [4.398517262085829, 52.003346279634798],
                [4.351433275357662, 52.003346279634385],
            ]
        )
        target_polygon = Polygon(  # EPSG:28992
            [
                [83878.604749474805431, 446614.971827268891502],
                [83919.412712014061981, 449476.480502580699977],
                [87150.449384919615113, 449431.446397167514078],
                [87111.496789666693076, 446569.919728695647791],
                [83878.604749474805431, 446614.971827268891502],
            ]
        )

        result: Polygon = tranform_polygon(source_polygon, "4326", "28992")

        self.assertIsNotNone(result)
        self.assertEqual(
            len(result.exterior.coords), len(target_polygon.exterior.coords)
        )
        for i in range(len(result.exterior.coords)):
            self.assertAlmostEqual(
                result.exterior.coords[i][0],
                target_polygon.exterior.coords[i][0],
                delta=1,
            )
            self.assertAlmostEqual(
                result.exterior.coords[i][1],
                target_polygon.exterior.coords[i][1],
                delta=1,
            )


if __name__ == "__main__":
    unittest.main()
