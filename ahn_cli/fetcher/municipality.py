import os

import geopandas as gpd
from geopandas import GeoDataFrame


def city_polygon(city_name: str) -> GeoDataFrame:
    """Return a polygon of the city's boundary."""
    s_city_name = city_name.lower()
    file_path = os.path.join(
        os.path.dirname(__file__), "data/municipality_simple.geojson"
    )

    municipality_df = gpd.read_file(file_path)

    # Filter the DataFrame based on lowercase column values
    filtered_df = municipality_df[
        municipality_df["name"].str.lower() == s_city_name
    ]
    if filtered_df.empty:
        raise ValueError(f"City {city_name} not found.")

    return filtered_df
