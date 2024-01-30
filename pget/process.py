import os
import tempfile

import numpy as np
from fetcher.request import Fetcher
from manipulator.point_cloud import LasPointCloud
import laspy
from laspy.lasappender import LasAppender

from manipulator.geojson import extract_polygon, read_geojson


def process(
    base_url: str,
    output_path: str,
    city_name: str,
    include_classes: list[int] | None = None,
    exclude_classes: list[int] | None = None,
    clip_file: str | None = None,
) -> None:
    # ahn_fetcher = Fetcher(base_url, city_name)
    # fetched_files = ahn_fetcher.fetch()
    fetched_files = {
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_14.LAZ": "./testdata/3.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_20.LAZ": "./testdata/5.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_01.LAZ": "./testdata/6.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_15.LAZ": "./testdata/4.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_02.LAZ": "./testdata/7.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_05.LAZ": "./testdata/0.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_03.LAZ": "./testdata/8.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_09.LAZ": "./testdata/1.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_16.LAZ": "./testdata/13.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_17.LAZ": "./testdata/14.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_10.LAZ": "./testdata/2.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_06.LAZ": "./testdata/9.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_07.LAZ": "./testdata/10.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_11.LAZ": "./testdata/11.LAZ",
    }
    files = list(fetched_files.values())
    print("files-----", files)

    points = np.array([])
    for file in files:
        las = laspy.read(file)
        print("las-------points:", len(las.points))
        pntc = LasPointCloud(las, "./pget/fetcher/data/municipality_simple.geojson")
        print("pntc-------points:", len(pntc.las.points))
        if include_classes is not None and len(include_classes) > 0:
            pntc.keep_classes(include_classes)
        print("pntc-------points:", len(pntc.las.points))
        if exclude_classes is not None and len(exclude_classes) > 0:
            pntc.exclude_classes(exclude_classes)
        print("pntc-------points:", len(pntc.las.points))
        if clip_file is not None:
            geojson = read_geojson(clip_file)
            polygon = extract_polygon(geojson)
            pntc.clip_by_polygon(polygon, geojson.crs)
        pntc.clip_by_city(city_name)
        las.points = pntc.build().points
        points = np.vstack((points, las.points))
    print("points-----", len(points))

    # with tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix=".tmp") as temp_f:
    #     laspy.read(files[0]).write(temp_f.name)
    #     las = laspy.read(temp_f.name)
    #     pc = LasPointCloud(
    #         las, temp_f, "./pget/fetcher/data/municipality_simple.geojson"  # type: ignore
    #     )
    #     print("las-------points:", len(pc.las.points))
    #     for file in list(files)[1:]:
    #         with laspy.open(file) as f:
    #             for points in f.chunk_iterator(1_000_000):
    #                 pc.merge(points)

    #     print("las-------points:", len(pc.las.points))
    #     point_cloud = pc
    #     if include_classes is not None and len(include_classes) > 0:
    #         point_cloud.keep_classes(include_classes)
    #     if exclude_classes is not None and len(exclude_classes) > 0:
    #         point_cloud.exclude_classes(exclude_classes)
    #     if clip_file is not None:
    #         geojson = read_geojson(clip_file)
    #         polygon = extract_polygon(geojson)
    #         point_cloud.clip_by_polygon(polygon, geojson.crs)
    #     point_cloud.clip_by_city(city_name)
    #     processed_las = point_cloud.build()

    #     processed_las.write(output_path)
    #     for file in list(fetched_files) + [temp_f.name]:
    #         os.remove(file)

    # with laspy.open(files[0]) as f:
    #     with laspy.open(files[1]) as f1:
    #         points = f.read().points
    #         print("f points:", len(points))
    #         f1las = f1.read()
    #         print("f1las points:", len(f1las.points))
    #         f1las.points = np.vstack((points, f1las.points))
    #         print("f1las points:", len(f1las.points))
