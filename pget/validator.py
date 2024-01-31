import os
import geopandas as gpd

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
    if cityname not in city_df["gemeentena"].str.lower().values:
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
            raise ValueError(f"Class {c} is in both include and exclude classes.")


def validate_clip_file(clip_file: str | None) -> str | None:
    if clip_file is None:
        return None
    if not os.path.exists(clip_file):
        raise ValueError("Clip file does not exist.")
    return clip_file


def validate_all(
    output_path: str,
    city_name: str,
    include_classes: list[int] | None = None,
    exclude_classes: list[int] | None = None,
    clip_file: str | None = None,
) -> bool:
    validate_output(output_path)
    validate_city(city_name, "../../ahn/data/municipality_simple.geojson")
    validate_include_classes(include_classes)
    validate_exclude_classes(exclude_classes)
    validate_include_exclude(include_classes, exclude_classes)
    validate_clip_file(clip_file)
    return True
