from importlib.resources import files
import geopandas as gpd
import unittest

from ahn_cli.manipulator import rasterizer

from ahn_cli.manipulator.transformer import tranform_polygon


TEST_DATA0 = "./tests/testdata/westervoort0_thinned.las"
TEST_DATA1 = "./tests/testdata/westervoort1_thinned.las"
CITY_FILE_PATH = "./ahn_cli/fetcher/data/municipality_simple.geojson"
WESTERVOORT_FILE_PATH = "./tests/testdata/westervoort.geojson"


class TestRasterize(unittest.TestCase):
    def test_rasterize(self) -> None:
        city_polygon_file = files("ahn_cli.fetcher.data").joinpath(
            "municipality_simple.geojson"
        )
        city_df = gpd.read_file(city_polygon_file)
        city_name = "Westervoort"
        record = city_df[city_df["name"].str.lower() == city_name.lower()]
        polygon = record.iloc[0].geometry
        crs = city_df.crs
        if crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        if polygon is None:
            raise ValueError("Failed to reproject polygon")
        rasterizer.polygon_to_raster(polygon, 50)


if __name__ == "__main__":
    unittest.main()
