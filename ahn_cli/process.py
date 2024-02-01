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
    preview: bool = False,
) -> None:
    ahn_fetcher = Fetcher(base_url, city_name)
    fetched_files = ahn_fetcher.fetch()
    files = list(fetched_files.values())

    pipeline = PntCPipeline(files[0], output_path, city_polygon_path)
    pipeline.merge(files[1:])
    if include_classes is not None and len(include_classes) > 0:
        pipeline.include(include_classes)
    if exclude_classes is not None and len(exclude_classes) > 0:
        pipeline.exclude(exclude_classes)
    if not no_clip_city:
        pipeline.clip(city_name)
    if clip_file is not None:
        pipeline.clip_by_arbitrary_polygon(clip_file)
    pipeline.execute()

    if preview:
        previewer(output_path)
