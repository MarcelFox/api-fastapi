from datetime import datetime

from fastapi.responses import JSONResponse

from src.app.rooms.model import Room, RoomModel
from src.app.rooms.repository import RoomRepository


class RoomController:
    def __init__(self):
        self.room_repository = RoomRepository()

    async def list_all_registered_rooms(self, skip: int, limit: int):
        return await self.room_repository.find_all(skip, limit)

    async def create_new_room(self, reservation: dict):
        found_room: RoomModel | None = await self.room_repository.find(reservation)
        code = 201 if found_room else 202
        if not found_room:
            await self.room_repository.insert(reservation)
        return JSONResponse(content=None, status_code=code)

    async def list_rooms_availability(self, id: str, start_time: str, end_time: str):
        room = await self.room_repository.find(({"id": id}))
        date_format = "%Y-%m-%dT%H:%M:%S"
        for reservation in room.reservations:
            if not (
                datetime.strptime(end_time, date_format) <= reservation.start_time
                or datetime.strptime(start_time, date_format) >= reservation.end_time
            ):
                return {"message": "room not available"}
        return {"message": "room available"}

    async def list_room_reservations(self, id: int, date: str):
        room = await self.room_repository.find({"id": id})
        if not room:
            return None
        if not date:
            return room.reservations
        return [
            _ for _ in room.reservations if _.start_time.strftime("%Y-%m-%d") == date
        ]
