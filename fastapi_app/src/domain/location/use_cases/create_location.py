import logging
from core.exceptions.database_exceptions import LocationAlreadyExistsException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationCreate, LocationResponseSchema

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
            with self._database.session() as session:
                created_location = self._location_repository.create(
                    session, location)

                created_location = self._location_repository.create(
                    session, location)

                return LocationResponseSchema.model_validate(created_location)
        except LocationAlreadyExistsException as e:
            logger.error(e.get_detail())
            raise e