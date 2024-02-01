import geopandas as gdp
from shapely.geometry import Polygon


def read_geojson(path: str) -> gdp.GeoDataFrame:
    gdf = gdp.read_file(path)
    return gdf


def extract_polygon(gdf: gdp.GeoDataFrame) -> Polygon | None:
    # return first polygon
    for geom in gdf.geometry:
        if geom.geom_type == "Polygon":
            return geom.coords[0]
    return None
