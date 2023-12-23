# import os
# import geopandas as gpd
# from municipality import city_polygon


# def ahn_tiles() -> gpd.GeoDataFrame:
#     file_path = os.path.join(os.path.dirname(__file__), "data/ahn_grid.geojson")

#     ahn_tile_gdf = gpd.read_file(file_path)
#     return ahn_tile_gdf


# def ahn_tile_indicies_of_city(city_name: str) -> list[str]:
#     """Return a list of AHN tile indicies that intersect with the city's boundary."""
#     city_poly = city_polygon(city_name)
#     ahn_tile_gdf = ahn_tiles()

#     # Filter the DataFrame based on lowercase column values
#     filtered_df = ahn_tile_gdf.overlay(city_poly)
#     tile_indices: list[str] = filtered_df["AHN"].tolist()  # type: ignore

#     return tile_indices
