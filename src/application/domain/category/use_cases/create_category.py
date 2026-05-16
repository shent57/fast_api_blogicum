import logging
from src.application.core.exceptions.database_exceptions import EntityAlreadyExistsException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from src.application.schemas.categories import CategoryCreate, CategoryResponseSchema

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(
            self, 
            category_repository: CategoryRepository, 
            database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(
            self, 
            category: CategoryCreate) -> CategoryResponseSchema:
        try:
            async with self._database.session() as session:
                created_category = self._category_repository.create(
                    session, 
                    category)

                return CategoryResponseSchema.model_validate(created_category)
        except EntityAlreadyExistsException as e:
            logger.error(e.get_detail())
            raise e