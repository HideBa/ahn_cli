import abc


class IClipper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def clip(self, url: str) -> str:
        raise NotImplementedError()
