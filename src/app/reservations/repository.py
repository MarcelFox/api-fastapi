import os
from typing import List

from src.app.reservations.model import Reservation, ReservationModel
from src.shared.repository import PostgresRepository


class ReservationRepository(PostgresRepository[Reservation]):
    def __init__(self):
        super().__init__(
            connection_url=os.getenv("POSTGRES_URL"), model=ReservationModel
        )
