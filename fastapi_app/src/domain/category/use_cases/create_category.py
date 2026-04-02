from datetime import datetime

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryCreate, CategoryResponseSchema


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
        with self._database.session() as session:
            created_category = self._category_repository.create(
                session, 
                category)

            created_at = (
                created_category.created_at
                if isinstance(created_category.created_at, datetime)
                else datetime.fromisoformat(created_category.created_at)
            )

            return CategoryResponseSchema.model_validate(created_category)