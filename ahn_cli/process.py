import os

import numpy as np
from ahn_cli.fetcher.request import Fetcher
from ahn_cli.manipulator.pipeline2 import PntCPipeline
from ahn_cli.manipulator.preview import previewer
import laspy
from laspy.lasappender import LasAppender


def process(
    base_url: str,
    city_polygon_path: str,
    output_path: str,
    city_name: str,
    include_classes: list[int] | None = None,
    exclude_classes: list[int] | None = None,
    no_clip_city: bool | None = False,
    clip_file: str | None = None,
    epsg: int | None = None,
    bbox: list[float] | None = None,
    radius: int | None = None,
    preview: bool | None = False,
) -> None:
    # ahn_fetcher = Fetcher(base_url, city_name)
    # fetched_files = ahn_fetcher.fetch()
    fetched_files = {
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_14.LAZ": "./testdata/3.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_20.LAZ": "./testdata/5.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_01.LAZ": "./testdata/6.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_15.LAZ": "./testdata/4.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_02.LAZ": "./testdata/7.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_03.LAZ": "./testdata/8.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_16.LAZ": "./testdata/13.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_17.LAZ": "./testdata/14.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_10.LAZ": "./testdata/2.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_06.LAZ": "./testdata/9.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_07.LAZ": "./testdata/10.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_11.LAZ": "./testdata/11.LAZ",
    }

    files = list(fetched_files.values())
    # maxs = np.array([0, 0, 0])  # [x, y, z]
    # mins = np.array([np.inf, np.inf, np.inf])  # [x, y, z]

    # for file in files:
    #     with laspy.open(file) as las:
    #         header = las.header
    #         print("header", header)
    #         print("offsets", las.header.offsets)
    #         print("scale", las.header.scales)
    #         maxs = np.maximum(maxs, las.header.maxs)
    #         mins = np.minimum(mins, las.header.mins)
    #         print("maxs", maxs)
    #         print("mins", mins)

    # TODO: Problem is that because each file has its own origin, relative position will be different
    for i, file in enumerate(files):
        with laspy.open(file) as las:
            if i == 0:
                global_header = las.header
            # update maxs and mins if necessary
            maxs = np.maximum(global_header.maxs, las.header.max)
            mins = np.minimum(global_header.mins, las.header.min)
            pipeline = PntCPipeline(las.read(), city_polygon_path, city_name)
            if bbox is not None:
                pipeline.clip_by_bbox(bbox)
            header = las.header
            offset = global_header.offsets - header.offsets
            print("offset", offset)

            if include_classes is not None and len(include_classes) > 0:
                pipeline.include(include_classes)
            if exclude_classes is not None and len(exclude_classes) > 0:
                pipeline.exclude(exclude_classes)
            if (
                not no_clip_city and radius is None
            ):  # if no radius is specified, clip by city
                print("a")
                # pipeline.clip()

            global_header.maxs = maxs
            global_header.mins = mins
            with laspy.open(
                output_path, mode="w" if i == 0 else "a", header=header
            ) as writer:
                print("writing points", len(pipeline.execute().points))
                points = pipeline.execute().points
                print("x shape", points.x.shape)
                points.x = points.x - offset[0]
                points.y = points.y - offset[1]
                points.z = points.z - offset[2]
                if isinstance(writer, laspy.LasWriter):
                    writer.write_points(points)
                if isinstance(writer, LasAppender):
                    writer.append_points(points)

    # for file in files:
    #     os.remove(file)

    if preview:
        print("Previewing output file...")
        previewer(output_path)
