from typing import BinaryIO, Self
import numpy as np
import laspy
from shapely.geometry import Point


from manipulator.polygon import DutchCity
from manipulator.transformer import tranform_polygon
from shapely.geometry import Polygon


class LasPointCloud:
    def __init__(self, las: laspy.LasData, city_polygon_file: str):
        self.las = las
        self.dutch_city = DutchCity(city_polygon_file, "name")

    def keep_classes(self, classes: list[int]) -> Self:
        # Build composite condition to filter out elements
        condition = np.isin(self.las.classification, classes)  # type: ignore
        self.las = self.las[condition]
        return self

    def exclude_classes(self, classes: list[int]) -> Self:
        # Build composite condition to filter out elements
        condition = np.isin(self.las.classification, classes, invert=True)  # type: ignore
        self.las = self.las[condition]
        return self

    # def merge(self, points: laspy.ScaleAwarePointRecord) -> Self:
    #     appender = LasAppender(self.source)
    #     appender.append_points(points)
    #     return self

    def clip_by_city(self, city_name: str) -> Self:
        city_polygon = self.dutch_city.city_polygon(city_name)
        polygon_crs = self.dutch_city.city_df.crs

        return self.clip_by_polygon(city_polygon, polygon_crs)

    def clip_by_polygon(self, polygon: Polygon, crs: str | None = None) -> Self:
        if crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        if polygon is None:
            raise ValueError("Failed to reproject polygon")
        points = self.las.xyz
        valid_points_indices = np.array([])
        for i, point in enumerate(points):
            print("progress:", (i / len(points)) * 100, "%")
            if polygon.contains([Point(point[0], point[1])]):
                valid_points_indices = np.append(valid_points_indices, i)
        valid_points = self.las.points[valid_points_indices]
        new_las = laspy.LasData(self.las.header, valid_points)  # type: ignore TODO: fix later
        self.las = new_las
        return self

    def build(self) -> laspy.LasData:
        return self.las
