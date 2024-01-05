import numpy as np
from polygon import DutchCity
import laspy

from transformer import tranform_polygon


def clip_pc_by_city(las: laspy.LasData, city_name: str) -> laspy.LasData:
    dutch_city = DutchCity("../../ahn/data/municipality_simple.geojson", "name")
    city_polygon = dutch_city.city_polygon(city_name)
    polygon_crs = dutch_city.city_df.crs
    TARGET_CRS = "EPSG:28992"
    # Memo: to suport other point cloud format, it needs to extract crs from point cloud data and convert polygon if needed

    reprojected_polygon = tranform_polygon(polygon_crs, TARGET_CRS, city_polygon)
    if reprojected_polygon is None:
        raise ValueError("Failed to reproject polygon")
    points = las.xyz
    valid_points_indices = np.array([])
    for i, point in points:
        if reprojected_polygon.contains([point[0], point[1]]):
            valid_points_indices = np.append(valid_points_indices, i)
    valid_points = las.points[valid_points_indices]
    new_las = laspy.LasData(las.header, valid_points)  # type: ignore TODO: fix later
    return new_las
