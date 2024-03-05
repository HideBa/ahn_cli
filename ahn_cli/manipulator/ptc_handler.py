from typing import Self

import geopandas as gpd
import laspy
import numpy as np
import rasterio
from shapely import Polygon

from ahn_cli.manipulator import rasterizer
from ahn_cli.manipulator.transformer import tranform_polygon


class PntCHandler:
    """
    A class for handling point clouds.

    Attributes:
        las (laspy.LasData): The point cloud data.
        city_df (gpd.GeoDataFrame): The city data.
        city_name (str): The name of the city.
        raster_res (float): The raster resolution.
        epsg (str | None): The EPSG code.

    Methods:
        __init__: Initializes the PntCHandler object.
        decimate: Decimates the point cloud by selecting every `step`-th point.
        include: Filters the point cloud to include only the specified classes.
        exclude: Exclude points with specific classification values from the pipeline.
        clip: Clip the point cloud by a polygon.
        clip_by_arbitrary_polygon: Clip the point cloud by an arbitrary polygon.
        clip_by_bbox: Clips the point cloud by a bounding box.
        points: Execute the pipeline and return the processed point cloud.
    """

    las = laspy.LasData
    city_df: gpd.GeoDataFrame
    city_name: str
    raster_res: float = 10.0  # default raster resolution
    epsg: str | None = None

    def __init__(
        self,
        las: laspy.LasData,
        city_filepath: str,
        city_name: str,
        epsg: int = 4326,
    ) -> None:
        self.las = las
        self.city_df = gpd.read_file(city_filepath)
        self.city_name = city_name
        self.epsg = "EPSG:" + str(epsg)

    def decimate(self, step: int) -> Self:
        """
        Decimates the point cloud by selecting every `step`-th point.

        Args:
            step (int): The decimation step size.

        Returns:
            Self: The modified pipeline object.
        """
        valid_point_masks = np.arange(0, len(self.las.points), step)
        self.las.points = self.las.points[valid_point_masks]
        return self

    def include(self, include_classes: list[int]) -> Self:
        """
        Filters the point cloud by including only the specified classes.

        Args:
            include_classes (list[int]): A list of class IDs to include.

        Returns:
            Self: The updated instance of the pipeline.
        """
        mask = np.isin(self.las.classification, include_classes)
        self.las.points = self.las.points[mask]
        return self

    def exclude(self, exclude_classes: list[int]) -> Self:
        """
        Exclude points from the point cloud based on their classification.

        Args:
            exclude_classes (list[int]): List of classification codes to exclude.

        Returns:
            Self: The modified pipeline object.

        """
        mask = np.isin(self.las.classification, exclude_classes, invert=True)
        self.las.points = self.las.points[mask]
        return self

    def clip(self) -> Self:
        """
        Clips the point cloud to the extent of the city polygon.

        Returns:
            Self: The modified pipeline object.
        """
        rasterized_polygon, transform = rasterizer.polygon_to_raster(
            self._city_polygon(), self.raster_res
        )

        xyz = self.las.xyz
        transformer = rasterio.transform.AffineTransformer(transform)
        rows, cols = transformer.rowcol(xyz[:, 0], xyz[:, 1])
        rows, cols = np.array(rows, dtype=int), np.array(cols, dtype=int)
        # Store original bounds checks
        original_rows_out_of_bounds = (rows < 0) | (
            rows >= rasterized_polygon.shape[0]
        )
        original_cols_out_of_bounds = (cols < 0) | (
            cols >= rasterized_polygon.shape[1]
        )

        rows = np.clip(rows, 0, rasterized_polygon.shape[0] - 1)
        cols = np.clip(cols, 0, rasterized_polygon.shape[1] - 1)
        valid_points_mask = (
            (rasterized_polygon[rows, cols] == 1)
            & (~original_rows_out_of_bounds)
            & (~original_cols_out_of_bounds)
        )
        self.las.points = self.las.points[valid_points_mask]
        return self

    def clip_by_arbitrary_polygon(self, clip_file: str) -> Self:
        """
        Clips the point cloud by an arbitrary polygon defined in a clip file.

        Args:
            clip_file (str): The path to the clip file containing the polygon.

        Returns:
            Self: The modified instance of the pipeline.
        """

        polygon = self._arbitrary_polygon(clip_file)
        rasterized_polygon, transform = rasterizer.polygon_to_raster(
            polygon, self.raster_res
        )

        xyz = self.las.xyz
        transformer = rasterio.transform.AffineTransformer(transform)
        rows, cols = transformer.rowcol(xyz[:, 0], xyz[:, 1])
        rows, cols = np.array(rows, dtype=int), np.array(cols, dtype=int)
        # Store original bounds checks
        original_rows_out_of_bounds = (rows < 0) | (
            rows >= rasterized_polygon.shape[0]
        )
        original_cols_out_of_bounds = (cols < 0) | (
            cols >= rasterized_polygon.shape[1]
        )

        rows = np.clip(rows, 0, rasterized_polygon.shape[0] - 1)
        cols = np.clip(cols, 0, rasterized_polygon.shape[1] - 1)
        valid_points_mask = (
            (rasterized_polygon[rows, cols] == 1)
            & (~original_rows_out_of_bounds)
            & (~original_cols_out_of_bounds)
        )
        self.las.points = self.las.points[valid_points_mask]
        return self

    def clip_by_bbox(self, bbox: list[float]) -> Self:
        """
        Clips the point cloud by a given bounding box.

        Args:
            bbox (list[float]): The bounding box coordinates in the format [xmin, ymin, xmax, ymax].

        Returns:
            Self: The modified instance of the pipeline.
        """

        x_valid = (self.las.x >= bbox[0]) & (self.las.x <= bbox[2])
        y_valid = (self.las.y >= bbox[1]) & (self.las.y <= bbox[3])
        valid_points_mask = np.where(x_valid & y_valid)[0]
        self.las.points = self.las.points[valid_points_mask]

        return self

    def points(self) -> laspy.LasData:
        """
        Returns the point cloud data.

        Returns:
            laspy.LasData: The point cloud data.
        """
        return self.las

    def _city_polygon(self) -> Polygon:
        """
        Retrieves the polygon for a given city name.

        Args:
            None
        Returns:
            Polygon: The polygon representing the city's boundary.
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
        if self.epsg is not None:
            polygon = tranform_polygon(polygon, self.epsg, "EPSG:28992")
        elif crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        if polygon is None:
            raise ValueError("Failed to reproject polygon")
        return polygon
