from typing import Annotated, Optional, TypedDict
from pydantic import BaseModel, BeforeValidator, Field

from src.shared.repository.mongo_repository import MongoRepository

PyObjectId = Annotated[str, BeforeValidator(str)]

class Room(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    capacity: int
    location: str

class RoomRepository(MongoRepository[Room]):
    def __init__(self):
        super().__init__(db_name='reservation_db', user="admin", password="password", collection_name='rooms')