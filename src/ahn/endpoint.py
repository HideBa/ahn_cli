import os
from constant import BASE_URL


def get_tile_endpoint(index: str) -> str:
    return os.path.join(BASE_URL + f"/03a_DSM_0.5m/{index}.zip")
