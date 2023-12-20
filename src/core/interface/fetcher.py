import abc


class IFetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch(self) -> bytearray:
        raise NotImplementedError()
