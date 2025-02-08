import os
from pydantic import BaseModel
from src.app.rooms.model import RoomModel
from src.shared.repository import PostgresRepository

class Room(BaseModel):
    name: str
    capacity: int
    location: str

class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    location: str

class RoomRepository(PostgresRepository[Room]):
    def __init__(self):
        super().__init__(connection_url=os.getenv('POSTGRES_URL'), model=RoomModel)