from dataclasses import dataclass


@dataclass
class Config:
    geotiles_base_url = "https://geotiles.citg.tudelft.nl/AHN4_T/"
    ahn_base_url = (
        "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/{tile_index}.zip"
    )
    city_polygon_file = "./ahn_cli/fetcher/data/municipality_simple.geojson"
