import abc


class IPointCloud(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def keep_classes(self, classes: list[int]) -> bytearray:
        raise NotImplementedError()

    def exclude_classes(self, classes: list[int]) -> bytearray:
        raise NotImplementedError()

    def merge(self, others: list[bytearray]) -> bytearray:
        raise NotImplementedError()

    def clip(self, clip_file: str) -> bytearray:
        raise NotImplementedError()

    def write(self, output: str) -> None:
        raise NotImplementedError()
