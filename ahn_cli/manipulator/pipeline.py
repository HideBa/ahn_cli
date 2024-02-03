import json
from typing import Any, Self

import geopandas as gpd
import pdal
from shapely import Polygon

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

    def __init__(
        self,
        input_path: str,
        output_path: str,
        city_filepath: str,
        city_name: str,
    ) -> None:
        self.pipeline_setting: list[Any] = []
        self._init_pipeline(input_path, output_path)
        self.city_df = gpd.read_file(city_filepath)
        self.city_name = city_name

    def _init_pipeline(self, input_path: str, output_path: str) -> Self:
        """
        Initialize the pipeline with the input and output settings.

        Args:
            input_path (str): The path to the input data.
            output_path (str): The path to save the output data.

        Returns:
            list: The initialized pipeline configuration.

        """
        self.pipeline_setting = [
            input_path,
            {
                "type": "writers.las",
                **(
                    {"compression": "laszip"}
                    if output_path.endswith(".laz")
                    or output_path.endswith("LAZ")
                    else {}
                ),
                "filename": output_path,
            },
        ]
        return self

    def merge(self, merge_files: list[str]) -> Self:
        """
        Merge the point cloud with another point cloud.

        Args:
            merge_file (str): The path to the point cloud file to merge.

        Returns:
            Pipeline: The updated pipeline object.

        """
        merge_pipe = [merge_file for merge_file in merge_files] + [
            {"type": "filters.merge"}
        ]
        self.pipeline_setting = (
            self.pipeline_setting[:1] + merge_pipe + self.pipeline_setting[1:]
        )
        return self

    def decimate(self, step: int) -> Self:
        """
        Decimate the point cloud by a given step.

        Args:
            step (int): The step to decimate by.

        Returns:
            Pipeline: The updated pipeline object.

        """
        decimate_pipe = [
            {
                "type": "filters.decimation",
                "step": str(step),
            }
        ]
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + decimate_pipe
            + self.pipeline_setting[-1:]
        )
        return self

    def include(self, include_classes: list[int]) -> Self:
        """
        Filters the point cloud to include only the specified classes.

        Args:
            include_classes (list[int]): List of class labels to include.

        Returns:
            Self: The modified pipeline object.
        """
        include_pipe = [
            {
                "type": "filters.range",
                "limits": ",".join(
                    [
                        "Classification[{}:{}]".format(
                            str(kclass), str(kclass)
                        )
                        for kclass in include_classes
                    ]
                ),
            },
        ]
        # append dbscan_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + include_pipe
            + self.pipeline_setting[-1:]
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
        # The reason why not using "filters.range" is because it doesn't work with multiple conditions for exclusion
        exclude_pipe = [
            {
                "type": "filters.expression",
                "expression": "&&".join(
                    [
                        "Classification != {}".format(str(ex_class))
                        for ex_class in exclude_classes
                    ]
                ),
            },
        ]

        # append dbscan_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + exclude_pipe
            + self.pipeline_setting[-1:]
        )
        return self

    def clip(self) -> Self:
        """
        Clip the point cloud by a polygon.

        Args:
            cityname (str): The name of the city to clip the point cloud.

        Returns:
            Self: The updated pipeline object.

        """
        city_polygon = self._city_polygon()
        clip_pipe = [
            {
                "type": "filters.crop",
                "polygon": city_polygon,
            }
        ]
        # append clip_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + clip_pipe
            + self.pipeline_setting[-1:]
        )
        return self

    def clip_by_arbitrary_polygon(self, clip_file: str) -> Self:
        """
        Clip the point cloud by a polygon.

        Args:
            clip_file (str): The path to the polygon file.

        Returns:
            Pipeline: The updated pipeline object.

        """
        clip_pipe = [
            {
                "type": "filters.crop",
                "polygon": self._arbitrary_polygon(clip_file),
            }
        ]
        # append clip_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + clip_pipe
            + self.pipeline_setting[-1:]
        )
        return self

    def clip_by_radius(self, radius: float) -> Self:
        """
        Clips the point cloud by a given radius around a specified center.

        Args:
            radius (float): The radius of the clipping area.

        Returns:
            Self: The modified instance of the pipeline.
        """
        record = self.city_df[
            self.city_df["name"].str.lower() == self.city_name.lower()
        ]
        polygon = record.iloc[0].geometry
        crs = self.city_df.crs
        if crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        center = polygon.centroid.coords[0]
        clip_pipe = [
            {
                "type": "filters.crop",
                "point": f"POINT({center[0]} {center[1]} 0)",
                "distance": str(radius),
            }
        ]

        # append clip_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + clip_pipe
            + self.pipeline_setting[-1:]
        )
        return self

    def info(self) -> Self:
        """
        Print the pipeline configuration.

        Returns:
            None
        """
        info_pipe = [
            {
                "type": "filters.info",
            }
        ]
        # append info_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:1] + info_pipe + self.pipeline_setting[1:]
        )
        return self

    def execute(self) -> None:
        """
        Execute the pipeline.

        Returns:
            None
        """
        print("Executing pipeline...")
        self.info()
        pipeline_json = json.dumps(self.pipeline_setting)
        pipeline = pdal.Pipeline(pipeline_json)
        pipeline.execute()
        log = pipeline.log
        print(log)

        print("Pipeline executed successfully")

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
        wkt_polygon = polygon.wkt
        return wkt_polygon

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
        city_df = gpd.read_file(filepath)
        polygon = city_df[city_df.geometry.type == "Polygon"].iloc[0].geometry
        crs = city_df.crs
        if crs is not None:
            polygon = tranform_polygon(polygon, crs, "EPSG:28992")
        if polygon is None:
            raise ValueError("Failed to reproject polygon")
        wkt_polygon = polygon.wkt
        return wkt_polygon

    def _clip_bbox(self, bbox: list[float]) -> Self:
        """
        Clip the point cloud by a bounding box.

        Args:
            bbox (list[float]): The bounding box to clip the point cloud. [xmin, ymin, xmax, ymax]

        Returns:
            Self: The updated pipeline object.

        """
        clip_pipe = [
            {
                "type": "filters.crop",
                "bounds": f"([{bbox[0]},{bbox[2]} ],[{bbox[1]},{bbox[3]}])",
            }
        ]

        # append clip_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1]
            + clip_pipe
            + self.pipeline_setting[-1:]
        )
        return self
