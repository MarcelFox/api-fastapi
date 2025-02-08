from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")
G = TypeVar("G")


class AbstractRepository(ABC, Generic[T]):
    def __init__(self, connection_url: str, model: Generic[G]):
        self.connection_url = connection_url
        self.model = model

    @abstractmethod
    def insert(self, data: dict) -> T | None:
        pass

    @abstractmethod
    def find(self, data: dict) -> Optional[T]:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, id: int, data: dict) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def execute(self, query: str) -> List[T] | T:
        pass
