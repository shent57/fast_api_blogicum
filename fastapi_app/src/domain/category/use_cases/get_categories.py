from datetime import datetime
from typing import List

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema


class GetCategoriesUseCase:
    def __init__(
            self, 
            category_repository: CategoryRepository, 
            database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(
        self, is_published: bool | None = None, title: str | None = None
    ) -> List[CategoryResponseSchema]:
        with self._database.session() as session:
            categories = self._category_repository.get_all(
                session, is_published)

            if is_published is not None:
                categories = [c 
                              for c in categories 
                              if c.is_published == is_published]

            if title is not None:
                categories = [c 
                              for c in categories 
                              if title.lower() in c.title.lower()]

            for c in categories:
                created_at = (
                    c.created_at
                    if isinstance(c.created_at, datetime)
                    else datetime.fromisoformat(c.created_at)
                )
            return [
                CategoryResponseSchema(
                    id=c.id,
                    title=c.title,
                    description=c.description,
                    slug=c.slug,
                    is_published=c.is_published,
                    created_at=created_at,
                    model="blog.category",
                )
                for c in categories
            ]
