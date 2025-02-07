from typing import List
from fastapi import APIRouter
from .controller import RoomController
from .repository import Room
from src.app.reservations.repository import Reservation

router = APIRouter()
room_controller = RoomController()

@router.get("/")
async def list_registered_rooms() -> List[Room]:
    return room_controller.list_all_registered_rooms()

@router.post("/")
async def room_registration(room: Room) -> str:
    return room_controller.create_new_room(room)

@router.get("/{id}/availability")
async def check_room_availability(id: str, start_time: str, end_time: str) -> dict:
    return room_controller.list_rooms_availability(id, start_time, end_time)