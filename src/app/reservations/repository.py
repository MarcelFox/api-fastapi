from typing import Annotated, Optional
from datetime import datetime
from pydantic import BaseModel, BeforeValidator, Field

from src.shared.repository.mongo_repository import MongoRepository

PyObjectId = Annotated[str, BeforeValidator(str)]

class Reservation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    room_id: str
    user_name: str
    start_time: datetime
    end_time: datetime

class ReservationRepository(MongoRepository[Reservation]):
    def __init__(self):
        super().__init__(db_name='reservation_db', user="admin", password="password", collection_name='reservations')