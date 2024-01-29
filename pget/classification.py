from enum import Enum


class AHNClassification(Enum):
    Created = 0
    Unclassified = 1
    Ground = 2
    Building = 6
    Water = 7
    HighTension = 14
    CivilStructure = 26

    def describe(self) -> str:
        return f"{self.name}, {self.value}"
