from core.interface.point_cloud import IPointCloud


class PointCloud(IPointCloud):
    def __init__(self, pdata: bytearray):
        self.pdata = pdata

    def keep_classes(self, classes: list[int]) -> bytearray:
        return bytearray()

    def exclude_classes(self, classes: list[int]) -> bytearray:
        return bytearray()
