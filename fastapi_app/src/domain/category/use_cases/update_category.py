from datetime import datetime

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema, CategoryUpdateData


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
        with self._database.session() as session:
            updated_category = self._category_repository.update(
                session, 
                category_id, 
                **category_data.model_dump(exclude_none=True)
            )

            created_at = (
                updated_category.created_at
                if isinstance(updated_category.created_at, datetime)
                else datetime.fromisoformat(updated_category.created_at)
            )
            return CategoryResponseSchema(
                id=updated_category.id,
                title=updated_category.title,
                description=updated_category.description,
                slug=updated_category.slug,
                is_published=updated_category.is_published,
                created_at=created_at,
                model="blog.category",
            )
