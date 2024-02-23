import time
import unittest

import laspy
import numpy as np

from ahn_cli.manipulator.pipeline import PntCPipeline

TEST_DATA0 = "./tests/testdata/westervoort0_thinned.las"
TEST_DATA1 = "./tests/testdata/westervoort1_thinned.las"
CITY_FILE_PATH = "./ahn_cli/fetcher/data/municipality_simple.geojson"
WESTERVOORT_FILE_PATH = "./tests/testdata/westervoort.geojson"
WESTERVOORT28992_FILE_PATH = "./tests/testdata/westervoort28992.geojson"


class TestPipeline(unittest.TestCase):
    def test_decimate(self) -> None:
        with laspy.open(TEST_DATA0) as reader:
            las = reader.read()
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort")
            points_before = len(pipeline.las.points)
            pipeline.decimate(10)
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)

    def test_include(self) -> None:
        with laspy.open(TEST_DATA0) as reader:
            las = reader.read()
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort")
            points_before = len(pipeline.las.points)
            pipeline.include([2, 6])
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)
            classes2 = len(las.points[las.classification == 2])
            classes6 = len(las.points[las.classification == 6])
            classes0 = len(las.points[las.classification == 0])
            classes1 = len(las.points[las.classification == 1])
            classes9 = len(las.points[las.classification == 9])
            classes26 = len(las.points[las.classification == 26])
            self.assertTrue(classes2 > 0)
            self.assertTrue(classes6 > 0)
            self.assertTrue(classes0 == 0)
            self.assertTrue(classes1 == 0)
            self.assertTrue(classes9 == 0)
            self.assertTrue(classes26 == 0)

    def test_exclude(self) -> None:
        with laspy.open(TEST_DATA0) as reader:
            las = reader.read()
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort")
            points_before = len(pipeline.las.points)
            pipeline.exclude([2, 6])
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)
            classes2 = len(las.points[las.classification == 2])
            classes6 = len(las.points[las.classification == 6])
            self.assertTrue(classes2 == 0)
            self.assertTrue(classes6 == 0)

    def test_clip(self) -> None:
        with laspy.open(TEST_DATA1) as reader:
            las = reader.read()
            extra_dim = laspy.ExtraBytesParams(name="raster", type=np.uint8)
            las.add_extra_dim(extra_dim)
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort")
            points_before = len(pipeline.las.points)
            pipeline.clip()
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)

    def test_clip_by_arbitrary_polygon(self) -> None:
        with laspy.open(TEST_DATA1) as reader:
            las = reader.read()
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort")
            points_before = len(pipeline.las.points)
            pipeline.clip_by_arbitrary_polygon(WESTERVOORT_FILE_PATH)
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)

        with laspy.open(TEST_DATA1) as reader:
            las = reader.read()
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort", 28992)
            points_before = len(pipeline.las.points)
            pipeline.clip_by_arbitrary_polygon(WESTERVOORT28992_FILE_PATH)
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)

    def test_clip_by_bbox(self) -> None:
        with laspy.open(TEST_DATA0) as reader:
            las = reader.read()
            pipeline = PntCPipeline(las, CITY_FILE_PATH, "Westervoort")
            points_before = len(pipeline.las.points)
            pipeline.clip_by_bbox(
                [194198.302994, 443461.343994, 194594.109009, 443694.838989]
            )
            points_after = len(pipeline.las.points)
            self.assertTrue(points_after < points_before)


if __name__ == "__main__":
    unittest.main()
