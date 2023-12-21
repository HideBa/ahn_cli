import abc


class IFetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch(self) -> list[bytearray]:
        raise NotImplementedError()
