from typing import Self
import numpy as np
import laspy
from laspy.lasappender import LasAppender


class LasPointCloud:
    def __init__(self, las: laspy.LasData):
        self.las = las

    def keep_classes(self, classes: list[int]) -> Self:
        # Build composite condition to filter out elements
        condition = np.isin(self.las.classification, classes)  # type: ignore
        self.las = self.las[condition]
        return self

    def exclude_classes(self, classes: list[int]) -> Self:
        # Build composite condition to filter out elements
        condition = np.isin(self.las.classification, classes, invert=True)  # type: ignore
        self.las = self.las[condition]
        return self

    def merge(self, others: laspy.LasData) -> Self:
        # appender = LasAppender
        # self.pc_data.append
        dims = self.las.point_format.dimension_names
        self.las = np.concatenate((self.las, others.points))

        return self

    def build(self) -> laspy.LasData:
        return self.las

    def clip(self, clip_file: str) -> np.ndarray:
        return np.array([])

    def write(self, output: str) -> None:
        return super().write(output)
