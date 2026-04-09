from typing import List
import logging
from core.exceptions.database_exceptions import CategoryNotFoundException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema

logger = logging.getLogger(__name__)


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
        try:
            with self._database.session() as session:
                categories = self._category_repository.get_all(
                    session, is_published)

                if is_published is not None:
                    categories = [
                        c 
                        for c in categories 
                        if c.is_published == is_published]

                if title is not None:
                    categories = [
                        c 
                        for c in categories 
                        if title.lower() in c.title.lower()]

                return [CategoryResponseSchema.model_validate(c) for c in categories]
        except CategoryNotFoundException as e:
            logger.error(e.get_detail())
            return []