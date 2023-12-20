import abc


class IPointCloud(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def keep_classes(self, classes: list[int]) -> bytearray:
        raise NotImplementedError()

    def exclude_classes(self, classes: list[int]) -> bytearray:
        raise NotImplementedError()
