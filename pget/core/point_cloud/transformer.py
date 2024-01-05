import pyproj
from shapely.ops import transform
import shapely


# Memo: hope to support more types of geometry
def tranform_polygon(
    geometry: shapely.Polygon, source_crs: str, target_crs: str
) -> shapely.Polygon | None:
    proj = pyproj.Transformer.from_crs(
        pyproj.CRS(f"epsg:{source_crs}"),
        pyproj.CRS(f"epsg:{target_crs}"),
        always_xy=True,
    ).transform
    if geometry.is_empty:
        return None
    elif geometry.geom_type == "Polygon":
        return transform(proj, geometry)
    return None
