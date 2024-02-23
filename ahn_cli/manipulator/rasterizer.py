from typing import Tuple

import numpy as np
from rasterio import features
from rasterio.transform import Affine, from_origin
from shapely import Polygon


def polygon_to_raster(
    polygon: Polygon,
    resolution: float,
) -> Tuple[np.ndarray, Affine]:
    """
    Convert a polygon to a raster file.

    Args:
        polygon (Polygon): The polygon to convert.
        resolution (float): The resolution of the raster.

    Returns:
        None

    """
    bbox = polygon.bounds
    height = int((bbox[3] - bbox[1]) / resolution)
    width = int((bbox[2] - bbox[0]) / resolution)

    transform = from_origin(bbox[0], bbox[3], resolution, resolution)
    shape = (height, width)
    rasterized = features.rasterize(
        shapes=[polygon],
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    )
    return rasterized, transform
