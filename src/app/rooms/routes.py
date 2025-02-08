from typing import List, Union
from fastapi import APIRouter
from .controller import RoomController
from .repository import Room, RoomResponse
from src.app.reservations.repository import ReservationResponse

router = APIRouter()
room_controller = RoomController()

@router.get("/")
async def list_registered_rooms() -> List[RoomResponse]:
    return await room_controller.list_all_registered_rooms()

@router.post("/")
async def room_registration(room: Room) -> RoomResponse:
    return await room_controller.create_new_room(vars(room))

@router.get("/{id}/availability")
async def check_room_availability(id: int, start_time: str, end_time: str) -> dict:
    return await room_controller.list_rooms_availability(id, start_time, end_time)

@router.get("/{id}/reservation")
async def check_room_availability(id: int, date: str = '') -> List[ReservationResponse]:
    return await room_controller.list_room_reservations(id, date)