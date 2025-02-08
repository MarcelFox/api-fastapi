from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.shared.classes import Base

class ReservationModel(Base):
    __tablename__ = 'reservations_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms_table.id'))

    room = relationship("RoomModel", back_populates="reservations", lazy='selectin')