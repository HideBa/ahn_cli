import os

import numpy as np
from ahn_cli.fetcher.request import Fetcher
from ahn_cli.manipulator.pipeline import PntCPipeline
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
    decimate: int | None = None,
    bbox: list[float] | None = None,
    preview: bool | None = False,
) -> None:
    ahn_fetcher = Fetcher(base_url, city_name)
    fetched_files = ahn_fetcher.fetch()

    files = list(fetched_files.values())
    for i, file in enumerate(files):
        with laspy.open(file) as las:
            if i == 0:
                global_header = las.header
            # update maxs and mins if necessary
            header = las.header
            offset = global_header.offsets - header.offsets
            maxs = np.maximum(global_header.maxs, las.header.max)
            mins = np.minimum(global_header.mins, las.header.min)
            global_header.maxs = maxs
            global_header.mins = mins

            pipeline = PntCPipeline(
                las.read(),
                city_polygon_path,
                city_name,
                epsg if epsg is not None else 4326,
            )

            if bbox is not None:
                pipeline.clip_by_bbox(bbox)
            if decimate is not None:
                pipeline.decimate(decimate)
            if include_classes is not None and len(include_classes) > 0:
                pipeline.include(include_classes)
            if exclude_classes is not None and len(exclude_classes) > 0:
                pipeline.exclude(exclude_classes)
            if not no_clip_city:
                pipeline.clip()
            if clip_file is not None:
                pipeline.clip_by_arbitrary_polygon(clip_file)

            with laspy.open(
                output_path, mode="w" if i == 0 else "a", header=global_header
            ) as writer:
                points = pipeline.points().points
                points.x = points.x - offset[0]
                points.y = points.y - offset[1]
                points.z = points.z - offset[2]
                if isinstance(writer, laspy.LasWriter):
                    writer.write_points(points)
                if isinstance(writer, LasAppender):
                    writer.append_points(points)

    for file in files:
        os.remove(file)

    if preview:
        print("Previewing output file...")
        previewer(output_path)
