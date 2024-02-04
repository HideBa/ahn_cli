import os

import geopandas as gpd

from ahn_cli.fetcher.municipality import city_polygon


def geotiles() -> gpd.GeoDataFrame:
    file_path = os.path.join(
        os.path.dirname(__file__), "data/ahn_subunit.geojson"
    )

    ahn_tile_gdf = gpd.read_file(file_path)
    return ahn_tile_gdf


def ahn_subunit_indicies_of_city(city_name: str) -> list[int]:
    """Return a list of AHN tile indicies that intersect with the city's boundary."""  # noqa
    city_poly = city_polygon(city_name)
    geotiles_tile_gdf = geotiles()

    # Filter the DataFrame based on lowercase column values
    filtered_df = geotiles_tile_gdf.overlay(city_poly)
    tile_indices: list[int] = filtered_df["AHN_subuni"].tolist()  # noqa

    return tile_indices