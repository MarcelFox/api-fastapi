from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.app.reservations.controller import ReservationsController
from src.app.reservations.repository import Reservation, ReservationResponse, ReservationsPaginated
from src.app.token.routes import get_current_active_user

router = APIRouter()
controller = ReservationsController()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/")
async def new_reservation(
    reservation: Reservation, user: Annotated[str, Depends(get_current_active_user)]
) -> ReservationResponse:
    date_format = "%Y-%m-%dT%H:%M:%S"
    wrong_time = reservation.start_time.strftime(
        date_format
    ) >= reservation.end_time.strftime(date_format)
    if wrong_time:
        raise HTTPException(status_code=406, detail="Wrong time.")
    registered = reservation.user_name == user.full_name
    if not registered:
        raise HTTPException(status_code=400, detail="Reservation user not registered")
    result = await controller.create_new_reservation(reservation)
    if type(result) == str:
        raise HTTPException(status_code=409, detail=result)
    if not result:
        raise HTTPException(status_code=500, detail="Something went wrong.")
    return result


@router.get("/")
async def get_reservations(skip: int = 0, limit: int = 10) -> ReservationsPaginated:
    total, reservations = await controller.get_reservations(skip, limit)
    return {"total": total, "skipping": skip, "limit": limit, "reservations": reservations}


@router.delete("/{id}")
async def remove_reservation(
    id: int, user: Annotated[str, Depends(get_current_active_user)]
):
    found_user = await controller.find_user_by_reservation_id(id)
    if not found_user:
        raise HTTPException(status_code=404, detail="Entity not found")
    if found_user != user.full_name:
        raise HTTPException(status_code=401, detail="Not authorized")
    await controller.remove_reservation(id)
    return JSONResponse(content="", status_code=204)
