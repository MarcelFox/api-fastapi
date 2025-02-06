from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def new_reservation():
    return {"message": "Hello Reservations!"}
