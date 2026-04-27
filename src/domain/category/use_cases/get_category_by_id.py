import logging
from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.infrastructure.sqlite.database import Database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.categories import CategoryResponseSchema

logger = logging.getLogger(__name__)


class GetCategoryByIdUseCase:
    def __init__(self, 
                 category_repository: CategoryRepository, 
                 database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        try:
            with self._database.session() as session:
                category = self._category_repository.get_by_id(
                    session, category_id)

                return CategoryResponseSchema.model_validate(category)
        except CategoryNotFoundException as e:
            logger.error(e.get_detail())
            raise e
        
        
        