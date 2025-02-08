import os
from datetime import datetime
from pydantic import BaseModel

from src.app.reservations.model import ReservationModel
from src.shared.repository import PostgresRepository

class Reservation(BaseModel):
    user_name: str = "John Doe"
    start_time: datetime = "2025-01-22T14:00:00"
    end_time: datetime = "2025-01-22T16:00:00"
    room_id: int

class ReservationResponse(BaseModel):
    id: int
    user_name: str
    start_time: datetime
    end_time: datetime
    room_id: int

class ReservationRepository(PostgresRepository[Reservation]):
    def __init__(self):
        super().__init__(connection_url=os.getenv("POSTGRES_URL"), model=ReservationModel)