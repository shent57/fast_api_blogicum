from typing import Type, List

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.models.categories import Category as CategoryModel
from schemas.categories import CategoryCreate as CategorySchema
from core.exceptions.database_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException



class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get_by_id(self, session: Session, category_id: int) -> CategoryModel:
        query = (
            select(self._model)
            .where(self._model.id == category_id)
        )

        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException()

        return category
    

    def get_by_slug(self, session: Session, slug: str) -> CategoryModel:
        query = (
            select(self._model)
            .where(self._model.slug == slug)
        )

        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException()

        return category
    
    def get_all(self, session: Session, is_published: bool | None = None) -> List[CategoryModel]:
        query = (
            select(self._model)
        )

        if is_published is not None:
            query = query.where(self._model.is_published == is_published)

        return list(session.scalars(query))
    

    def create(self, session: Session, category: CategorySchema) -> CategoryModel:
        query = (
            insert(self._model)
            .values(**category.model_dump())
            .returning(self._model)
        )

        try:
            category = session.scalar(query)
        except IntegrityError:
            raise CategoryAlreadyExistsException()

        return category
    

    def update(self, session: Session, category_id: int, **kwargs) -> CategoryModel:
        category = self.get_by_id(session, category_id)

        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)

        session.commit()

        return category
    

    def delete(self, session: Session, category_id: int) -> None:
        category = self.get_by_id(session, category_id)
        session.delete(category)