import logging
from src.application.core.exceptions.database_exceptions import EntityAlreadyExistsException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from src.application.schemas.locations import LocationCreate, LocationResponseSchema

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(
            self, 
            location: LocationCreate) -> LocationResponseSchema:
        try:
            async with self._database.session() as session:
                created_location = self._location_repository.create(
                    session, location)

                created_location = self._location_repository.create(
                    session, location)

                return LocationResponseSchema.model_validate(created_location)
        except EntityAlreadyExistsException as e:
            logger.error(e.get_detail())
            raise e