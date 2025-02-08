from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.shared.classes import Base

class RoomModel(Base):
    __tablename__ = 'rooms_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship("ReservationModel", back_populates="room", lazy='selectin')