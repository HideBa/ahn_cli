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
    no_clip_city: bool = False,
    clip_file: str | None = None,
    radius: int | None = None,
    preview: bool = False,
) -> None:
    # ahn_fetcher = Fetcher(base_url, city_name)
    # fetched_files = ahn_fetcher.fetch()

    fetched_files = {
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_14.LAZ": "./testdata/3.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_20.LAZ": "./testdata/5.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_01.LAZ": "./testdata/6.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_15.LAZ": "./testdata/4.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_02.LAZ": "./testdata/7.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_05.LAZ": "./testdata/0.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_03.LAZ": "./testdata/8.LAZ",
        # "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_09.LAZ": "./testdata/1.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_16.LAZ": "./testdata/13.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_17.LAZ": "./testdata/14.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ1_10.LAZ": "./testdata/2.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_06.LAZ": "./testdata/9.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_07.LAZ": "./testdata/10.LAZ",
        "https://geotiles.citg.tudelft.nl/AHN4_T/40BZ2_11.LAZ": "./testdata/11.LAZ",
    }

    files = list(fetched_files.values())

    print("radius ", radius)
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

    # for file in files:
    #     os.remove(file)

    if preview:
        print("Previewing output file...")
        previewer(output_path)
