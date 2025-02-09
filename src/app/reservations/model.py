from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.shared.classes import Base


class ReservationModel(Base):
    __tablename__ = "reservations_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms_table.id"))

    room = relationship("RoomModel", back_populates="reservations", lazy="selectin")


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


class ReservationsPaginated(BaseModel):
    total: int
    skipping: int
    limit: int
    reservations: List[ReservationResponse]
