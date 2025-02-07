from typing import List
from fastapi import APIRouter
from .controller.room_controller import RoomController
from .repository.room_repository import Room

router = APIRouter()
controller = RoomController()

@router.get("/")
async def list_registered_rooms() -> List[Room]:
    return controller.list_all_registered_rooms()

@router.post("/")
async def room_registration(room: Room) -> str:
    return controller.create_new_room(room)

@router.get("/{id}/availability")
async def check_room_availability(id: int):
    return {"message": f"Room {id} is available!"}