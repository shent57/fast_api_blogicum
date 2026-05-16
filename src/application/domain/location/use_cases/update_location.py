import logging

from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from src.application.schemas.locations import LocationResponseSchema, LocationUpdateData

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(
        self, location_id: int, location_data: LocationUpdateData
    ) -> LocationResponseSchema:
        try:
            async with self._database.session() as session:
                updated_location = self._location_repository.update(
                    session, 
                    location_id, 
                    **location_data.model_dump(exclude_none=True)
                )

                return LocationResponseSchema.model_validate(updated_location)
        except EntityNotFoundException as e:
            logger.error(e.get_detail())
            raise e