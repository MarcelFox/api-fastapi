from src.app.rooms.repository.room_repository import RoomRepository, Room


class RoomController():
    def __init__(self):
        self.room_repository = RoomRepository()

    def list_all_registered_rooms(self):
         return self.room_repository.find_all()
    
    def create_new_room(self, room: Room):       
        found_room: Room | None = self.room_repository.find_one(query=room.__dict__)
        if found_room:
            return f"{found_room['_id']}"
        return self.room_repository.insert_one(room.__dict__)
