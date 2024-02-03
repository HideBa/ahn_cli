import os
import tempfile
import unittest

import laspy

from ahn_cli.manipulator.pipeline import PntCPipeline

TEST_DATA0 = "./ahn_cli/test/testdata/westervoort0_thinned.las"
TEST_DATA1 = "./ahn_cli/test/testdata/westervoort1_thinned.las"
CITY_FILE_PATH = "./ahn_cli/fetcher/data/municipality_simple.geojson"
WESTERVOORT_FILE_PATH = "./ahn_cli/test/testdata/westervoort.geojson"


class TestPipeline(unittest.TestCase):
    def test_laz(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".laz", delete=True) as tmp:
            # check if file exists
            self.assertTrue(tmp.name)
            self.assertTrue(os.path.exists(TEST_DATA0))

            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertEqual(points_after, points_before)

    def test_decimate(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.decimate(10)
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertTrue(points_after < points_before)

    def test_include(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.include([2, 6])
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
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
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.exclude([2, 6])
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertTrue(points_after < points_before)

                classes2 = len(las.points[las.classification == 2])
                classes6 = len(las.points[las.classification == 6])
                self.assertTrue(classes2 == 0)
                self.assertTrue(classes6 == 0)

    def test_merge(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.merge([TEST_DATA1])
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertTrue(points_after > points_before)

    def test_clip(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.clip()
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertTrue(points_after < points_before)

    def test_clip_by_arbitrary_polygon(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.clip_by_arbitrary_polygon(WESTERVOORT_FILE_PATH)
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertTrue(points_after < points_before)

    def test_clip_by_radius(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".las", delete=True) as tmp:
            pipeline = PntCPipeline(
                TEST_DATA0, tmp.name, CITY_FILE_PATH, "Westervoort"
            )
            pipeline.clip_by_radius(1000)
            pipeline.execute()

            with laspy.open(TEST_DATA0) as las:
                points_before = las.header.point_count
                las = laspy.read(tmp.name)
                points_after = las.header.point_count
                self.assertTrue(points_after < points_before)


if __name__ == "__main__":
    unittest.main()
