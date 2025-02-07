from src.app.reservations.repository import Reservation, ReservationRepository
from src.app.rooms.repository import Room, RoomRepository


class ReservationsController():
    def __init__(self):
        self.room_repository = ReservationRepository()
    
    def create_new_room(self, reservation: Reservation):  
        found_room: Reservation | None = self.room_repository.find_one(query=reservation.__dict__)
        if found_room:
            return f"{found_room['_id']}"
        return self.room_repository.insert_one(reservation.__dict__)
