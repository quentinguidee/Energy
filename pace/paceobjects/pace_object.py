from abc import abstractmethod, ABCMeta


class PaceObject(metaclass=ABCMeta):
    id: int = None

    @property
    @abstractmethod
    def template_filename(self) -> str:
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        pass

    @property
    @abstractmethod
    def replace_queries(self) -> dict:
        pass
