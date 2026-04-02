from datetime import datetime

from core.exceptions.database_exceptions import LocationNotFoundException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema


class GetLocationByIdUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(self, location_id: int) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._location_repository.get_by_id(
                session, 
                location_id)

            if not location:
                raise LocationNotFoundException()

            return LocationResponseSchema.model_validate(location)