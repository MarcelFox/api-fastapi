import os
from typing import List

from pydantic import BaseModel

from src.app.rooms.model import RoomModel
from src.shared.repository import PostgresRepository


class Room(BaseModel):
    name: str = "Sala 1"
    capacity: int
    location: str = "Andar 1"


class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    location: str

class RoomsPaginated(BaseModel):
    total: int
    skipping: int
    limit: int
    rooms: List[RoomResponse]


class RoomRepository(PostgresRepository[Room]):
    def __init__(self):
        super().__init__(connection_url=os.getenv("POSTGRES_URL"), model=RoomModel)
