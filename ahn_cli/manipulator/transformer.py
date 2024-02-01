import pyproj
import shapely
from shapely.ops import transform


# Memo: hope to support more types of geometry
def tranform_polygon(
    geometry: shapely.Polygon, source_crs: str, target_crs: str
) -> shapely.Polygon | None:
    proj = pyproj.Transformer.from_crs(
        pyproj.CRS(source_crs),
        pyproj.CRS(target_crs),
        always_xy=True,
    ).transform
    if geometry.is_empty:
        return None
    elif geometry.geom_type == "Polygon":
        return transform(proj, geometry)
    return None
