import os

import geopandas as gpd
from pyproj import Transformer

from ahn_cli.fetcher.municipality import city_polygon


def geotiles() -> gpd.GeoDataFrame:
    file_path = os.path.join(
        os.path.dirname(__file__), "data/ahn_subunit.geojson"
    )

    ahn_tile_gdf = gpd.read_file(file_path)
    return ahn_tile_gdf


def ahn_subunit_indicies_of_city(city_name: str) -> list[str]:
    """Return a list of AHN tile indicies that intersect with the city's boundary."""  # noqa
    city_poly = city_polygon(city_name)
    geotiles_tile_gdf = geotiles()

    # Filter the DataFrame based on lowercase column values
    filtered_df = geotiles_tile_gdf.overlay(city_poly)
    tile_indices: list[str] = filtered_df["AHN_subuni"].tolist()  # noqa

    return tile_indices


def ahn_subunit_indicies_of_bbox(bbox: list[float]) -> list[str]:
    """Return a list of AHN tile indicies that intersect with the bbox."""  # noqa
    geotiles_tile_gdf = geotiles()

    transformer = Transformer.from_crs(
        "EPSG:28992", "EPSG:4326", always_xy=True
    )
    minx, miny = transformer.transform(bbox[0], bbox[1])
    maxx, maxy = transformer.transform(bbox[2], bbox[3])
    # Filter the DataFrame based on lowercase column values
    filtered_df = geotiles_tile_gdf.cx[minx:maxx, miny:maxy]
    tile_indices: list[str] = filtered_df["AHN_subuni"].tolist()  # noqa

    return tile_indices
