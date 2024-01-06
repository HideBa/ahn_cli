import os
import tempfile
from ahn.fetcher import Fetcher
from core.point_cloud.point_cloud import LasPointCloud
import laspy

from core.point_cloud.geojson import extract_polygon, read_geojson


# class Service:
#     def __init__(self, las_path: str, base_url: str, city_name: str, output_path: str):
#         self.fetcher = Fetcher(base_url, city_name)
#         self.las_path = las_path
#         self.output_path = output_path


def process(
    base_url: str,
    output_path: str,
    city_name: str,
    include_classes: list[int] | None = None,
    exclude_classes: list[int] | None = None,
    clip_file: str | None = None,
) -> None:
    ahn_fetcher = Fetcher(base_url, city_name)
    fetched_files = ahn_fetcher.fetch()
    las = laspy.read(fetched_files[list(fetched_files)[0]])
    with tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix=".tmp") as temp_f:
        pc = LasPointCloud(
            las, temp_f, "../../ahn/data/municipality_simple.geojson"  # type: ignore
        )
        for file in list(fetched_files)[1:]:
            with laspy.open(file) as f:
                for points in f.chunk_iterator(1_000_000):  # type: ignore
                    pc.merge(points)

        point_cloud = LasPointCloud(
            las, fetched_files[0], "../../ahn/data/municipality_simple.geojson"
        )
        if include_classes is not None:
            point_cloud.keep_classes(include_classes)
        if exclude_classes is not None:
            point_cloud.exclude_classes(exclude_classes)
        if clip_file is not None:
            geojson = read_geojson(clip_file)
            polygon = extract_polygon(geojson)
            point_cloud.clip_by_polygon(polygon, geojson.crs)
        point_cloud.clip_by_city(city_name)
        processed_las = point_cloud.build()

        processed_las.write(output_path)
        for file in list(fetched_files) + [temp_f.name]:
            os.remove(file)
