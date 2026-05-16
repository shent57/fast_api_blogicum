from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
import logging
from src.application.core.exceptions.database_exceptions import EntityNotFoundException

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(self, location_id: int) -> None:
        try:
            async with self._database.session() as session:
                self._location_repository.delete(session, location_id)
        except EntityNotFoundException as e:
            logger.error(e.get_detail())
            raise e