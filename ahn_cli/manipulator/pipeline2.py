import json
from typing import Any, Iterable, Self, Tuple
import numpy as np
from shapely import Point
import geopandas as gpd
import pdal
from shapely import Polygon
from ahn_cli.manipulator import rasterizer
import rasterio
from rasterio.io import BufferedDatasetWriterBase
import laspy

from ahn_cli.manipulator.transformer import tranform_polygon


class PntCPipeline:
    """
    A class representing a data processing pipeline.

    Args:
        input_path (str): The path to the input data.
        output_path (str): The path to save the output data.
        city_filepath (str): The path to the city data file.
        city_name (str): The name of the city.

    Attributes:
        pipeline_setting (list): The configuration settings for the pipeline.

    """

    las = laspy.LasData
    city_df: gpd.GeoDataFrame
    city_name: str
    raster_res: float = 50.0  # default raster resolution
    epsg: str | None = None

    def __init__(
        self,
        las: laspy.LasData,
        city_filepath: str,
        city_name: str,
        epsg: int = 28992,
    ) -> None:
        self.las = las
        self.city_df = gpd.read_file(city_filepath)
        self.city_name = city_name
        self.epsg = "EPSG:" + str(epsg)

    def decimate(self, step: int) -> Self:
        """
        Decimate the point cloud by a given step.

        Args:
            step (int): The step to decimate by.

        Returns:
            Pipeline: The updated pipeline object.

        """
        self.las.points = self.las.points[::step]
        return self

    def include(self, include_classes: list[int]) -> Self:
        """
        Filters the point cloud to include only the specified classes.

        Args:
            include_classes (list[int]): List of class labels to include.

        Returns:
            Self: The modified pipeline object.
        """
        mask = np.isin(self.las.classification, include_classes)
        self.las.points = self.las.points[mask]
        print(
            "before",
            len(self.las.classification),
            "after",
            len(self.las.points),
        )
        return self

    def exclude(self, exclude_classes: list[int]) -> Self:
        """
        Exclude points with specific classification values from the pipeline.

        Args:
            exclude_classes (list[int]): List of classification values to exclude.

        Returns:
            Self: The modified pipeline object.
        """
        mask = np.isin(self.las.classification, exclude_classes, invert=True)
        self.las.points = self.las.points[mask]
        print(
            "before",
            len(self.las.classification),
            "after",
            len(self.las.points),
        )
        return self

    # def clip(self) -> Self:
    #     """
    #     Clip the point cloud by a polygon.
    #     """
    #     rasterized_polygon, transform = rasterizer.polygon_to_raster(
    #         self._city_polygon(), self.raster_res
    #     )

    #     xyz = self.las.xyz
    #     points = self.las.points
    #     valid_points_mask = np.zeros((len(xyz),), dtype=np.uint8)
    #     transformer = rasterio.transform.AffineTransformer(transform)
    #     for i, point in enumerate(xyz):
    #         # row, col = self.map_to_grid(point[0], point[1], transform)
    #         row, col = transformer.rowcol(point[0], point[1])
    #         if (
    #             row < 0
    #             or row >= rasterized_polygon.shape[0]
    #             or col < 0
    #             or col >= rasterized_polygon.shape[1]
    #         ):
    #             valid_points_mask[i] = 0
    #         else:
    #             if rasterized_polygon[row, col] != 1:
    #                 valid_points_mask[i] = 0
    #             else:
    #                 valid_points_mask[i] = 1
    #     self.las.raster = valid_points_mask
    #     print("valid points", len(valid_points_mask))
    #     print("valid points", valid_points_mask)
    #     return self

    def clip(self) -> Self:
        """
        Clip the point cloud by a polygon.
        """
        rasterized_polygon, transform = rasterizer.polygon_to_raster(
            self._city_polygon(), self.raster_res
        )

        xyz = self.las.xyz

        transformer = rasterio.transform.AffineTransformer(transform)
        rows, cols = transformer.rowcol(xyz[:, 0], xyz[:, 1])
        valid_points_mask = rasterized_polygon[rows, cols] == 1
        self.las.points = self.las.points[valid_points_mask].copy()

        print("before", len(xyz), "after", len(self.las.points))
        return self

    # def clip2(self) -> Self:
    #     points = self.las.xyz
    #     polygon = self._city_polygon()
    #     for i, point in enumerate(points):
    #         if not polygon.contains([Point(point[0], point[1])]):
    #             point = None
    #     return self

    def clip_by_arbitrary_polygon(self, clip_file: str) -> Self:
        """
        Clip the point cloud by a polygon.

        Args:
            clip_file (str): The path to the polygon file.

        Returns:
            Pipeline: The updated pipeline object.

        """
        polygon = self._arbitrary_polygon(clip_file)
        rasterized_polygon, transform = rasterizer.polygon_to_raster(
            polygon, self.raster_res
        )

        xyz = self.las.xyz
        grid_coords = np.array(~transform * (xyz[:, :2].T))
        rows, cols = grid_coords.astype(int)

        rows = np.clip(rows, 0, rasterized_polygon.shape[0] - 1)
        cols = np.clip(cols, 0, rasterized_polygon.shape[1] - 1)

        valid_points_mask = rasterized_polygon[rows, cols] == 1
        self.las.points = self.las.points[valid_points_mask]

        print("before", len(xyz), "after", len(self.las.points))
        return self

    def clip_by_bbox(self, bbox: list[float]) -> Self:
        """
        Clips the point cloud by a bounding box.

        Args:
            bbox (list[float]): The bounding box to clip the point cloud. [xmin, ymin, xmax, ymax]

        Returns:
            Self: The updated pipeline object.

        """
        xyz = self.las.xyz
        x_valid = (xyz[0] >= bbox[0]) & (xyz[0] <= bbox[2])
        y_valid = (xyz[1] >= bbox[1]) & (xyz[1] <= bbox[3])
        print("first point---------", xyz[0])
        valid_points_mask = np.where(x_valid & y_valid)
        print("valid points", len(valid_points_mask))
        self.las.points = self.las.points[valid_points_mask]
        return self

    def execute(self) -> laspy.LasData:
        """
        Execute the pipeline.

        Returns:
            laspy.LasData: The processed point cloud.
        """

        print("Pipeline executed successfully")
        return self.las

    def _city_polygon(self) -> Polygon:
        """
        Retrieves the polygon for a given city name.

        Args:
            None
        Returns:
            str: The well-known text (WKT) representation of the city's polygon.
        Raises:
            ValueError: If the polygon fails to be reprojected.
        """
        record = self.city_df[
            self.city_df["name"].str.lower() == self.city_name.lower()
        ]
        polygon = record.iloc[0].geometry
        crs = self.city_df.crs
        if crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        if polygon is None:
            raise ValueError("Failed to reproject polygon")
        return polygon

    def _arbitrary_polygon(self, filepath: str) -> Polygon:
        """
        Reads a file containing city data, extracts the first polygon geometry,
        transforms it to a specific coordinate reference system (CRS), and returns
        the well-known text (WKT) representation of the polygon.

        Args:
            filepath (str): The path to the file containing city data.

        Returns:
            str: The well-known text (WKT) representation of the polygon.

        Raises:
            ValueError: If the polygon fails to be reprojected.
        """
        gdf = gpd.read_file(filepath)
        polygon = gdf[gdf.geometry.type == "Polygon"].iloc[0].geometry
        crs = gdf.crs
        if crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        if self.epsg is not None:
            polygon = tranform_polygon(polygon, self.epsg, "EPSG:28992")
        if polygon is None:
            raise ValueError("Failed to reproject polygon")
        return polygon
