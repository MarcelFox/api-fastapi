from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.app.reservations.controller import ReservationsController
from src.app.reservations.repository import Reservation, ReservationResponse

router = APIRouter()
controller = ReservationsController()


@router.post("/")
async def new_reservation(reservation: Reservation) -> ReservationResponse:
    return await controller.create_new_room(vars(reservation))


@router.get("/")
async def get_reservations() -> List[ReservationResponse]:
    return await controller.get_reservations()


@router.delete("/{id}")
async def remove_reservation(id: int):
    await controller.remove_reservation(id)
    return JSONResponse(content="", status_code=204)
