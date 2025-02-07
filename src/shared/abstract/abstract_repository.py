from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class AbstractRepository(ABC, Generic[T]):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        pass

    @abstractmethod
    def insert(self, entity: T) -> T | None:
        pass

    @abstractmethod
    def find(self, entity: T, id: str) -> Optional[T]:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, id: str, data: dict) -> T:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def execute(self, query: str) -> List[T] | T:
        pass