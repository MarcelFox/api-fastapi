import os
from typing import List

from src.app.rooms.model import Room, RoomModel
from src.shared.repository import PostgresRepository


class RoomRepository(PostgresRepository[Room]):
    def __init__(self):
        super().__init__(connection_url=os.getenv("POSTGRES_URL"), model=RoomModel)
