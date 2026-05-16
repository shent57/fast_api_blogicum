from typing import List, Type

from src.application.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException, EntityNotFoundException)
from src.application.infrastructure.postgres.models.categories import Category as CategoryModel
from src.application.schemas.categories import CategoryCreate as CategorySchema
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    async def get_by_id(self, session: AsyncSession, category_id: int) -> CategoryModel:
        try:
            query = select(self._model).where(self._model.id == category_id)

            category = await session.scalar(query)
            if not category:
                raise EntityNotFoundException(detail=f"Категория с id='{category_id}' не найдена")
            return category
        except SQLAlchemyError:
            raise

    async def get_by_slug(self, session: AsyncSession, slug: str) -> CategoryModel:
        try:
            query = select(self._model).where(self._model.slug == slug)

            category = await session.scalar(query)
            if not category:
                raise EntityNotFoundException(detail=f"Категория с slug='{slug}' не найдена")
            return category
        except SQLAlchemyError:
            raise

    async def get_all(
        self, session: AsyncSession, is_published: bool | None = None
    ) -> List[CategoryModel]:
        try:
            query = select(self._model)

            if is_published is not None:
                query = query.where(self._model.is_published == is_published)

            return list(await session.scalars(query))
        except SQLAlchemyError:
            raise

    async def create(self, 
               session: AsyncSession, 
               category: CategorySchema) -> CategoryModel:
        query = (
            insert(self._model)
            .values(**category.model_dump())
            .returning(self._model)
        )

        try:
            category_obj = await session.scalar(query)
            await session.commit()
            return category_obj
        except IntegrityError:
            await session.rollback()
            raise EntityAlreadyExistsException(detail=f"Категория с slug='{category.slug}' уже существует")
        except SQLAlchemyError:
            await session.rollback()
            raise

    async def update(self, 
               session: AsyncSession, 
               category_id: int, **kwargs) -> CategoryModel:
        try:
            category = self.get_by_id(session, category_id)

            for key, value in kwargs.items():
                if hasattr(category, key):
                    setattr(category, key, value)

            await session.commit()
            return category
        except SQLAlchemyError:
            raise

    async def delete(self, session: AsyncSession, category_id: int) -> None:
        try:
            category = self.get_by_id(session, category_id)
            await session.delete(category)
            await session.commit()
        except SQLAlchemyError:
            raise