import os
import geopandas as gpd

from ahn_cli import config

AHN_CLASSES = [0, 1, 2, 6, 7, 4, 6]


def validate_output(output: str) -> str:
    if output is None:
        raise ValueError("Output path is required.")
    if not os.path.exists(os.path.dirname(output)):
        raise ValueError("Output directory does not exist.")
    return output


def validate_city(cityname: str, cityfile_path: str) -> str:
    if cityname is None:
        raise ValueError("City name is required.")
    city_df = gpd.read_file(cityfile_path)
    if cityname.lower() not in city_df["name"].str.lower().tolist():
        raise ValueError("City name not found in city list.")
    return cityname


def validate_include_classes(classes: list[int] | None) -> list[int] | None:
    if classes is None:
        return None
    for c in classes:
        if c not in AHN_CLASSES:
            raise ValueError(f"Class {c} is not a valid AHN class.")
    return classes


def validate_exclude_classes(classes: list[int] | None) -> list[int] | None:
    if classes is None:
        return None
    for c in classes:
        if c not in AHN_CLASSES:
            raise ValueError(f"Class {c} is not a valid AHN class.")
    return classes


def validate_include_exclude(
    include_classes: list[int] | None, exclude_classes: list[int] | None
) -> None:
    if include_classes is None or exclude_classes is None:
        return
    for c in include_classes:
        if c in exclude_classes:
            raise ValueError(
                f"Class {c} is in both include and exclude classes."
            )


def validate_clip_file(clip_file: str | None) -> str | None:
    if clip_file is None:
        return None
    if not os.path.exists(clip_file):
        raise ValueError("Clip file does not exist.")
    return clip_file


def validate_epsg(epsg: int | None) -> int | None:
    if epsg is None:
        return None
    if epsg < 1000 or epsg > 999999:
        raise ValueError("EPSG code is not valid.")
    return epsg


def validate_decimate(decimate: int | None) -> int | None:
    if decimate is None:
        return None
    if decimate < 1:
        raise ValueError("Decimate must be greater than 0.")
    return decimate


def validate_bbox(bbox: list[float] | None) -> list[float] | None:
    if bbox is None:
        return None
    if len(bbox) != 4:
        raise ValueError("Bounding box must have 4 coordinates.")
    if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
        raise ValueError("Bounding box coordinates are not valid.")
    return bbox


def validate_all(
    cfg: config.Config,
    output_path: str,
    city_name: str,
    include_classes: list[int] | None = None,
    exclude_classes: list[int] | None = None,
    no_clip_city: bool | None = False,
    clip_file: str | None = None,
    epsg: int | None = None,
    decimate: int | None = None,
    bbox: list[float] | None = None,
) -> bool:
    validate_output(output_path)
    if not bbox:
        validate_city(city_name, cfg.city_polygon_file)
    validate_include_classes(include_classes)
    validate_exclude_classes(exclude_classes)
    validate_include_exclude(include_classes, exclude_classes)
    validate_clip_file(clip_file)
    validate_epsg(epsg)
    validate_decimate(decimate)
    validate_bbox(bbox)
    return True
