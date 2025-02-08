from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.app.reservations.repository import ReservationResponse

from .controller import RoomController
from .repository import Room, RoomResponse, RoomsPaginated

router = APIRouter()
room_controller = RoomController()


@router.get("/")
async def list_registered_rooms(skip: int = 0, limit: int = 10) -> RoomsPaginated:
    total, rooms = await room_controller.list_all_registered_rooms(skip, limit)
    return {"total": total, "limit": limit, "rooms": rooms}

@router.post("/")
async def room_registration(room: Room) -> RoomResponse:
    return await room_controller.create_new_room(vars(room))


@router.get("/{id}/availability")
async def check_room_availability(id: int, start_time: str, end_time: str) -> dict:
    try:
        date_format = "%Y-%m-%dT%H:%M:%S"
        wrong_time = datetime.strptime(start_time, date_format) >= datetime.strptime(
            end_time, date_format
        )
        if wrong_time:
            raise ValueError
        return await room_controller.list_rooms_availability(id, start_time, end_time)
    except ValueError:
        raise HTTPException(status_code=406, detail="Wrong time")


@router.get("/{id}/reservation")
async def check_room_availability(
    id: int, date: str = None
) -> List[ReservationResponse]:
    try:
        if date:
            datetime.strptime(date, "%Y-%m-%d")
        result = await room_controller.list_room_reservations(id, date)
        if not result:
            raise HTTPException(status_code=404, detail="Room not found.")
        return result
    except ValueError:
        raise HTTPException(status_code=406, detail="Wrong time format")
