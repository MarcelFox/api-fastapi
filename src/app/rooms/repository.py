from pydantic import BaseModel

from src.shared.repository import PostgresRepository

class Room(BaseModel):
    id: str
    name: str
    capacity: int
    location: str

class RoomRepository(PostgresRepository[Room]):
    def __init__(self):
        super().__init__(db_name='reservation_db', user="admin", password="password", collection_name='rooms')