import os
from ahn_cli.fetcher.request import Fetcher
from ahn_cli.manipulator.pipeline import PntCPipeline
from ahn_cli.manipulator.preview import previewer


def process(
    base_url: str,
    city_polygon_path: str,
    output_path: str,
    city_name: str,
    include_classes: list[int] | None = None,
    exclude_classes: list[int] | None = None,
    no_clip_city: bool | None = False,
    clip_file: str | None = None,
    radius: int | None = None,
    preview: bool | None = False,
) -> None:
    ahn_fetcher = Fetcher(base_url, city_name)
    fetched_files = ahn_fetcher.fetch()

    files = list(fetched_files.values())

    pipeline = PntCPipeline(
        files[0], output_path, city_polygon_path, city_name
    )
    pipeline.merge(files[1:])
    if radius is not None:
        pipeline.clip_by_radius(radius)
    if include_classes is not None and len(include_classes) > 0:
        pipeline.include(include_classes)
    if exclude_classes is not None and len(exclude_classes) > 0:
        pipeline.exclude(exclude_classes)
    if (
        not no_clip_city and radius is None
    ):  # if no radius is specified, clip by city
        pipeline.clip()
    if clip_file is not None:
        pipeline.clip_by_arbitrary_polygon(clip_file)
    pipeline.execute()

    for file in files:
        os.remove(file)

    if preview:
        print("Previewing output file...")
        previewer(output_path)
