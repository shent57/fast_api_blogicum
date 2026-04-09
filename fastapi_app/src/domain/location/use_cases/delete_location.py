from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository
import logging
from core.exceptions.database_exceptions import LocationNotFoundException

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(self, location_id: int) -> None:
        try:
            with self._database.session() as session:
                self._location_repository.delete(session, location_id)
        except LocationNotFoundException as e:
            logger.error(e.get_detail())
            raise e