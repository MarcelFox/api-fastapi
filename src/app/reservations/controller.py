from typing import List

from src.app.reservations.repository import (ReservationModel,
                                             ReservationRepository)


class ReservationsController:
    def __init__(self):
        self.reservations_repository = ReservationRepository()

    async def get_reservations(self):
        data: List[ReservationModel] = await self.reservations_repository.find_all()
        for el in data:
            print(el.room.name)
        return data

    async def remove_reservation(self, id: int):
        return await self.reservations_repository.delete(id)
