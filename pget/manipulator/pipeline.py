from typing import Any, Self


class Pipeline:
    """
    A class representing a data processing pipeline.

    Args:
        input_path (str): The path to the input data.
        output_path (str): The path to save the output data.
        output_extra_dims (list, optional): A list of extra dimensions to include in the output data. Defaults to [].

    Attributes:
        pipeline_setting (list): The configuration settings for the pipeline.

    """

    def __init__(self, input_path: str, output_path: str) -> None:
        self.pipeline_setting: list[Any] = []
        self._init_pipeline(input_path, output_path)

    def _init_pipeline(self, input_path: str, output_path: str) -> Self:
        """
        Initialize the pipeline with the input and output settings.

        Args:
            input_path (str): The path to the input data.
            output_path (str): The path to save the output data.
            output_extra_dims (list, optional): A list of extra dimensions to include in the output data. Defaults to [].

        Returns:
            list: The initialized pipeline configuration.

        """
        self.pipeline_setting: list[Any] = [
            input_path,
            {
                "type": "writers.las",
                "filename": output_path,
            },
        ]
        return self

    def keep(self, keep_classes: list[int]) -> Self:
        keep_pipe = [
            {
                "type": "filters.range",
                "limits": ",".join(
                    [
                        "Classification[{}:{}]".format(str(kclass), str(kclass))
                        for kclass in keep_classes
                    ]
                ),
            },
        ]
        # append dbscan_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1] + keep_pipe + self.pipeline_setting[-1:]
        )
        return self

    def exclude(self, exclude_classes: list[int]) -> Self:
        ex_classes = [
            {
                "type": "filters.range",
                "limits": ",".join(
                    [
                        "!Classification[{}:{}]".format(str(ex_class), str(ex_class))
                        for ex_class in exclude_classes
                    ]
                ),
            },
        ]

        # append dbscan_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1] + exclude_classes + self.pipeline_setting[-1:]
        )
        return self

    def clip(self, clip_file: str) -> Self:
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
                "filename": clip_file,
            }
        ]
        # append clip_pipe to pipeline_setting as -2 index. This is because the last index is the writer
        self.pipeline_setting = (
            self.pipeline_setting[:-1] + clip_pipe + self.pipeline_setting[-1:]
        )
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

    def execute(self) -> None:
        """
        Execute the pipeline.

        Returns:
            int: The number of points processed by the pipeline.

        """
        print("Executing pipeline...")
        print("Pipeline: ", self.pipeline_setting)
        pipeline_json = json.dumps(self.pipeline_setting)
        print("Pipeline json: ", pipeline_json)
        pipeline = pdal.Pipeline(pipeline_json)
        count = pipeline.execute()
        arrays = pipeline.arrays
        metadata = pipeline.metadata
        log = pipeline.log

        print("Pipeline executed successfully")
        print("Point count: ", count)
        # print("Arrays: ", arrays)
        # print("Metadata: ", metadata)
