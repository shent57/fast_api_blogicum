import logging
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from src.application.schemas.categories import CategoryResponseSchema, CategoryUpdateData

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(
            self, 
            category_repository: CategoryRepository, 
            database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(
        self, category_id: int, category_data: CategoryUpdateData
    ) -> CategoryResponseSchema:
        try:
            async with self._database.session() as session:
                updated_category = self._category_repository.update(
                    session, 
                    category_id, 
                    **category_data.model_dump(exclude_none=True)
                )
                return CategoryResponseSchema.model_validate(updated_category)
        except EntityNotFoundException as e:
            logger.error(e.get_detail())
            raise e