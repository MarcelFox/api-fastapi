from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class AbstractRepository(ABC, Generic[T]):
    def __init__(self, db_name: str, user: str, password: str, host: str, port: str):
        """Initialize the repository connection."""
        pass

    @abstractmethod
    def insert_one(self, entity: T) -> str:
        """Insert a single entity into the storage."""
        pass

    @abstractmethod
    def find_one(self, query: dict) -> Optional[T]:
        """Find a single entity matching the query."""
        pass

    @abstractmethod
    def find_all(self, query: dict = {}) -> List[T]:
        """Find all entities matching the query."""
        pass

    @abstractmethod
    def update_one(self, query: dict, update: dict) -> int:
        """Update a single entity matching the query."""
        pass

    @abstractmethod
    def delete_one(self, query: dict) -> int:
        """Delete a single entity matching the query."""
        pass
