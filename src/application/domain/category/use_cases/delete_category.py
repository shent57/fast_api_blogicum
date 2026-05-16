from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
import logging
from src.application.core.exceptions.database_exceptions import EntityNotFoundException

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(
            self, 
            category_repository: CategoryRepository, 
            database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(self, category_id: int) -> None:
        try:
            async with self._database.session() as session:
                self._category_repository.delete(session, category_id)
        except EntityNotFoundException as e:
            logger.error(e.get_detail())
            raise e