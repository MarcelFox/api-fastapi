from datetime import datetime
from typing import List

from sqlalchemy.exc import IntegrityError

from src.app.reservations.repository import (Reservation, ReservationModel,
                                             ReservationRepository)


class ReservationsController:
    def __init__(self):
        self.reservations_repository = ReservationRepository()

    async def get_reservations(self, skip: int, limit: int):
        return await self.reservations_repository.find_all(skip, limit)

    async def create_new_reservation(
        self, reservation: Reservation
    ) -> Reservation | str | None:
        try:
            reservation_exists = await self.__check_if_reservation_exists(
                reservation.room_id, reservation.start_time, reservation.end_time
            )
            if reservation_exists:
                return "Reservation already exists"
            return await self.reservations_repository.insert(vars(reservation))
        except IntegrityError:
            return None

    async def find_user_by_reservation_id(self, id: int) -> str:
        try:
            reservation = await self.reservations_repository.find({"id": id})
            if not reservation:
                return None
            return reservation.user_name
        except IntegrityError:
            return None

    async def __check_if_reservation_exists(
        self, room_id: int, start_time: datetime, end_time: datetime
    ) -> bool:
        found_reservation = await self.reservations_repository.find(
            {"room_id": room_id}
        )
        if not found_reservation:
            return False
        if not (
            end_time <= found_reservation.start_time
            or start_time >= found_reservation.end_time
        ):
            return True
        return False

    async def remove_reservation(self, id: int):
        return await self.reservations_repository.delete(id)
