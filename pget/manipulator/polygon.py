import geopandas as gpd
from shapely.geometry import Polygon


class DutchCity:
    def __init__(self, filepath: str, column_name: str):
        self.filepath = filepath
        self.column_name = column_name
        self.city_df = gpd.read_file(self.filepath)

    def city_polygon(self, city_name: str) -> Polygon:
        record = self.city_df[
            self.city_df[self.column_name].str.lower() == city_name.lower()
        ]
        return record.iloc[0].geometry
