from datetime import datetime

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema, LocationUpdateData


class UpdateLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(
        self, location_id: int, location_data: LocationUpdateData
    ) -> LocationResponseSchema:
        with self._database.session() as session:
            updated_location = self._location_repository.update(
                session, 
                location_id, 
                **location_data.model_dump(exclude_none=True)
            )

            created_at = (
                updated_location.created_at
                if isinstance(updated_location.created_at, datetime)
                else datetime.fromisoformat(updated_location.created_at)
            )

            return LocationResponseSchema(
                id=updated_location.id,
                name=updated_location.name,
                is_published=updated_location.is_published,
                created_at=created_at,
                model="blog.location",
            )
