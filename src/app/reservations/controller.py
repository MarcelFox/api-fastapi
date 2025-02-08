from typing import List

from sqlalchemy.exc import IntegrityError

from src.app.reservations.repository import (Reservation, ReservationModel,
                                             ReservationRepository)


class ReservationsController:
    def __init__(self):
        self.reservations_repository = ReservationRepository()

    async def get_reservations(self, skip: int, limit: int):
        return await self.reservations_repository.find_all(skip, limit)

    async def create_new_reservation(self, reservation: Reservation) -> Reservation:
        try:
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

    async def remove_reservation(self, id: int):
        return await self.reservations_repository.delete(id)
