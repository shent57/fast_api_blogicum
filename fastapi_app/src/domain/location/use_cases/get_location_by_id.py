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

            created_at = (
                location.created_at
                if isinstance(location.created_at, datetime)
                else datetime.fromisoformat(location.created_at)
            )

            return LocationResponseSchema(
                id=location.id,
                name=location.name,
                is_published=location.is_published,
                created_at=created_at,
                model="blog.location",
            )
