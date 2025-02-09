from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.shared.classes import Base


class RoomModel(Base):
    __tablename__ = "rooms_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship(
        "ReservationModel", back_populates="room", lazy="selectin"
    )


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
