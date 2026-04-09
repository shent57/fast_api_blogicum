from typing import List, Type

from core.exceptions.database_exceptions import (
    LocationAlreadyExistsException, LocationNotFoundException)
from infrastructure.sqlite.models.locations import Location as LocationModel
from schemas.locations import LocationCreate as LocationSchema
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class LocationRepository:
    def __init__(self):
        self._model: Type[LocationModel] = LocationModel

    def get_by_id(self, session: Session, location_id: int) -> LocationModel:
        try:
            query = select(self._model).where(self._model.id == location_id)

            location = session.scalar(query)
            if not location:
                raise LocationNotFoundException()

            return location
        except SQLAlchemyError:
            raise LocationNotFoundException(location_id=location_id)

    def get_all(
        self, session: Session, is_published: bool | None = None
    ) -> List[LocationModel]:
        try:
            query = select(self._model)

            if is_published is not None:
                query = query.where(self._model.is_published == is_published)

            return list(session.scalars(query))
        except SQLAlchemyError:
            return []

    def create(
            self, 
            session: Session, 
            location: LocationSchema) -> LocationModel:
        query = (
            insert(self._model)
            .values(**location.model_dump())
            .returning(self._model)
        )

        try:
            location_obj = session.scalar(query)
            session.commit()
            return location_obj
        except IntegrityError:
            session.rollback()
            raise LocationAlreadyExistsException(name=location.name)
        except SQLAlchemyError:
            session.rollback()
            raise LocationAlreadyExistsException(name=location.name)

    def update(
            self, 
            session: Session, 
            location_id: int, **kwargs) -> LocationModel:
        try:
            location = self.get_by_id(session, location_id)

            for key, value in kwargs.items():
                if hasattr(location, key):
                    setattr(location, key, value)

            session.commit()
            return location
        except SQLAlchemyError:
            session.rollback()
            raise LocationNotFoundException(location_id=location_id)

    def delete(self, session: Session, location_id: int) -> None:
        try:
            location = self.get_by_id(session, location_id)
            session.delete(location)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise LocationNotFoundException(location_id=location_id)