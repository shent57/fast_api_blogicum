import logging
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from src.application.schemas.locations import LocationResponseSchema

logger = logging.getLogger(__name__)


class GetLocationByIdUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(self, location_id: int) -> LocationResponseSchema:
        try:
            async with self._database.session() as session:
                location = self._location_repository.get_by_id(
                    session, 
                    location_id)

                return LocationResponseSchema.model_validate(location)
        except EntityNotFoundException as e:
            logger.error(e.get_detail())
            raise e