from typing import TypeVar, List, Optional
from src.shared.abstract import AbstractRepository

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

T = TypeVar('T')

class MongoRepository(AbstractRepository[T]):
    def __init__(self, db_name: str, user: str, password:str, collection_name: str, host: str = "0.0.0.0"):
        super().__init__(db_name, user, password, host)
        self.client = MongoClient(f'mongodb://{user}:{password}@{host}')
        self.db: Database = self.client[db_name]
        self.collection: Collection = self.db[collection_name]
    
    def insert_one(self, entity: T) -> str:
        return str(self.collection.insert_one(entity).inserted_id)

    def find_one(self, query: dict) -> Optional[T]:
        return self.collection.find_one(query)

    def find_all(self, query: dict = {}) -> List[T]:
        return list(self.collection.find({}))

    def update_one(self, query: dict, update: dict) -> int:
        return self.collection.update_one(query, {'$set': update}).modified_count

    def delete_one(self, query: dict) -> int:
        return self.collection.delete_one(query).deleted_count

    def close_connection(self):
        """Close the database connection."""
        self.client.close()