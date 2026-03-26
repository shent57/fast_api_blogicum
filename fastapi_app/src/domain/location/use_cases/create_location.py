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

            created_at = (
                created_location.created_at
                if isinstance(created_location.created_at, datetime)
                else datetime.fromisoformat(created_location.created_at)
            )

            return LocationResponseSchema(
                id=created_location.id,
                name=created_location.name,
                is_published=created_location.is_published,
                created_at=created_at,
                model="blog.location",
            )
