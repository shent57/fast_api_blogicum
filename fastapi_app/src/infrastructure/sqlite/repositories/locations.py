from typing import Type, List

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.models.locations import Location as LocationModel
from schemas.locations import LocationCreate as LocationSchema
from core.exceptions.database_exceptions import LocationNotFoundException, LocationAlreadyExistsException


class LocationRepository:
    def __init__(self):
        self._model: Type[LocationModel] = LocationModel
    
    def get_by_id(self, session: Session, location_id: int) -> LocationModel:
        query = (
            select(self._model)
            .where(self._model.id == location_id)
        )

        location = session.scalar(query)
        if not location:
            raise LocationNotFoundException()

        return location
    

    def get_all(self, session: Session, is_published: bool | None = None) -> List[LocationModel]:
        query = select(self._model)

        if is_published is not None:
            query = query.where(self._model.is_published == is_published)

        return list(session.scalars(query))
    
    def create(self, session: Session, location: LocationSchema) -> LocationModel:
        query = (
            insert(self._model)
            .values(**location.model_dump())
            .returning(self._model)
        )

        try:
            location = session.scalar(query)
        except IntegrityError:
            raise LocationAlreadyExistsException()

        return location
    
    def update(self, session: Session, location_id: int, **kwargs) -> LocationModel:
        location = self.get_by_id(session, location_id)

        for key, value in kwargs.items():
            if hasattr(location, key):
                setattr(location, key, value)

        session.flush()

        return location
    
    def delete(self, session: Session, location_id: int) -> None:
        location = self.get_by_id(session, location_id)
        session.delete(location)