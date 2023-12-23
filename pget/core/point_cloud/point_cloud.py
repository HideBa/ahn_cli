from core.interface.point_cloud import IPointCloud


class LazPointCloud(IPointCloud):
    def __init__(self, pdata: bytearray):
        self.pdata = pdata

    def keep_classes(self, classes: list[int]) -> bytearray:
        pipeline = [
            {
                "type": "filters.range",
                "limits": "Classification[{}]".format(
                    ",".join(str(c) for c in classes)
                ),
            }
        ]
        return bytearray()

    def exclude_classes(self, classes: list[int]) -> bytearray:
        pipeline = [
            {
                "type": "filters.range",
                "limits": "Classification![{}]".format(
                    ",".join(str(c) for c in classes)
                ),
            }
        ]
        return bytearray()

    def merge(self, others: list[bytearray]) -> bytearray:
        pipeline = [
            {
                "type": "filters.merge",
                "inputs": [
                    self.pdata,
                    *[other for other in others],
                ],
            }
        ]
        return bytearray()

    def clip(self, clip_file: str) -> bytearray:
        return bytearray()

    def write(self, output: str) -> None:
        return super().write(output)
