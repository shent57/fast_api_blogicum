from typing import List, Type

from core.exceptions.database_exceptions import (
    CategoryAlreadyExistsException, CategoryNotFoundException)
from infrastructure.sqlite.models.categories import Category as CategoryModel
from schemas.categories import CategoryCreate as CategorySchema
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get_by_id(self, session: Session, category_id: int) -> CategoryModel:
        try:
            query = select(self._model).where(self._model.id == category_id)

            category = session.scalar(query)
            if not category:
                raise CategoryNotFoundException(category_id=category_id)

            return category
        except SQLAlchemyError:
            raise CategoryNotFoundException(category_id=category_id)

    def get_by_slug(self, session: Session, slug: str) -> CategoryModel:
        try:
            query = select(self._model).where(self._model.slug == slug)

            category = session.scalar(query)
            if not category:
                raise CategoryNotFoundException(slug=slug)

            return category
        except SQLAlchemyError:
            raise CategoryNotFoundException(slug=slug)
        

    def get_all(
        self, session: Session, is_published: bool | None = None
    ) -> List[CategoryModel]:
        try:
            query = select(self._model)

            if is_published is not None:
                query = query.where(self._model.is_published == is_published)

            return list(session.scalars(query))
        except SQLAlchemyError:
            return []

    def create(self, 
               session: Session, 
               category: CategorySchema) -> CategoryModel:
        query = (
            insert(self._model)
            .values(**category.model_dump())
            .returning(self._model)
        )

        try:
            category_obj = session.scalar(query)
            session.commit()
            return category_obj
        except IntegrityError:
            session.rollback()
            raise CategoryAlreadyExistsException(slug=category.slug)
        except SQLAlchemyError:
            session.rollback()
            raise CategoryAlreadyExistsException(slug=category.slug)

    def update(self, 
               session: Session, 
               category_id: int, **kwargs) -> CategoryModel:
        try:
            category = self.get_by_id(session, category_id)

            for key, value in kwargs.items():
                if hasattr(category, key):
                    setattr(category, key, value)

            session.commit()
            return category
        except SQLAlchemyError:
            session.rollback()
            raise CategoryNotFoundException(category_id=category_id)

    def delete(self, session: Session, category_id: int) -> None:
        try:
            category = self.get_by_id(session, category_id)
            session.delete(category)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise CategoryNotFoundException(category_id=category_id)