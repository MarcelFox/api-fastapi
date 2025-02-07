from src.app.rooms.repository import RoomRepository, Room
from src.app.reservations.repository import Reservation, ReservationRepository
from datetime import datetime


class RoomController():
    def __init__(self):
        self.room_repository = RoomRepository()
        self.reservation_repository = ReservationRepository()

    def list_all_registered_rooms(self):
         return self.room_repository.find_all()
    
    def create_new_room(self, room: Room):       
        found_room: Room | None = self.room_repository.find_one(query=room.__dict__)
        if found_room:
            return f"{found_room['_id']}"
        return self.room_repository.insert_one(room.__dict__)
    
    def list_rooms_availability(self, id: str, start_time: str, end_time: str):
        reservations = self.reservation_repository.find_all({'_id': id})
        date_format = "%Y-%m-%dT%H:%M:%S"
        for booking in reservations:
            if not (datetime.strptime(end_time, date_format) <= booking['start_time'] or datetime.strptime(start_time, date_format) >= booking['end_time']):
                return {"message": "room not available"}
        return {"message": "room available"}
