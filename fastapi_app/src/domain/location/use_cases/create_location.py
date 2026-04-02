from datetime import datetime

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationCreate, LocationResponseSchema


class CreateLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(
            self, 
            location: LocationCreate) -> LocationResponseSchema:
        with self._database.session() as session:
            created_location = self._location_repository.create(
                session, location)

            created_location = self._location_repository.create(session, location)

            return LocationResponseSchema.model_validate(created_location)