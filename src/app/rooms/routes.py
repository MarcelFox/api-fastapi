from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_registered_rooms():
    return {"message": "Hello Rooms!"}

@router.post("/")
async def room_registration():
    return {"message": "Room registered!"}

@router.get("/{id}/availability")
async def check_room_availability(id: int):
    return {"message": f"Room {id} is available!"}