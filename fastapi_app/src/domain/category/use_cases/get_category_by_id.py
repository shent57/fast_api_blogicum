from datetime import datetime

from core.exceptions.database_exceptions import CategoryNotFoundException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema


class GetCategoryByIdUseCase:
    def __init__(self, 
                 category_repository: CategoryRepository, 
                 database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._category_repository.get_by_id(
                session, category_id)

            if not category:
                raise CategoryNotFoundException()

            created_at = (
                category.created_at
                if isinstance(category.created_at, datetime)
                else datetime.fromisoformat(category.created_at)
            )

            return CategoryResponseSchema(
                id=category.id,
                title=category.title,
                description=category.description,
                slug=category.slug,
                is_published=category.is_published,
                created_at=created_at,
                model="blog.category",
            )
