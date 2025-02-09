from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.app.reservations.repository import ReservationsPaginated

from .controller import RoomController
from .repository import Room, RoomResponse, RoomsPaginated

router = APIRouter()
room_controller = RoomController()


@router.get("/")
async def list_registered_rooms(skip: int = 0, limit: int = 10) -> RoomsPaginated:
    total, rooms = await room_controller.list_all_registered_rooms(skip, limit)
    return {"total": total, "skipping": skip, "limit": limit, "rooms": rooms}


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
async def list_room_reservations(
    id: int, date: str = None, skip: int = 0, limit: int = 10
) -> ReservationsPaginated:
    try:
        if date:
            datetime.strptime(date, "%Y-%m-%d")
        result = await room_controller.list_room_reservations(id, date)
        if not result:
            raise HTTPException(status_code=404, detail="Reservations not found")
        return {
            "total": len(result),
            "skipping": skip,
            "limit": limit,
            "reservations": result[skip : skip + limit],
        }
    except ValueError:
        raise HTTPException(status_code=406, detail="Wrong time format")
