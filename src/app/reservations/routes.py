from fastapi import APIRouter

from src.app.reservations.controller import ReservationsController
from src.app.reservations.repository import Reservation

router = APIRouter()
controller = ReservationsController()

@router.post("/")
async def new_reservation(reservation: Reservation):
    return controller.create_new_room(reservation)
