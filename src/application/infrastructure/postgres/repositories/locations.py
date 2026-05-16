from typing import List, Type

from src.application.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException, EntityNotFoundException)
from src.application.infrastructure.postgres.models.locations import Location as LocationModel
from src.application.schemas.locations import LocationCreate as LocationSchema
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class LocationRepository:
    def __init__(self):
        self._model: Type[LocationModel] = LocationModel

    async def get_by_id(self, session: AsyncSession, location_id: int) -> LocationModel:
        try:
            query = select(self._model).where(self._model.id == location_id)

            location = await session.scalar(query)
            if not location:
                raise EntityNotFoundException(detail=f"Локация с id='{location_id}' не найдена")
            return location
        except SQLAlchemyError:
            raise

    async def get_all(
        self, session: AsyncSession, is_published: bool | None = None
    ) -> List[LocationModel]:
        try:
            query = select(self._model)

            if is_published is not None:
                query = query.where(self._model.is_published == is_published)

            return list(await session.scalars(query))
        except SQLAlchemyError:
            raise

    async def create(
            self, 
            session: AsyncSession, 
            location: LocationSchema) -> LocationModel:
        query = (
            insert(self._model)
            .values(**location.model_dump())
            .returning(self._model)
        )

        try:
            location_obj = await session.scalar(query)
            await session.commit()
            return location_obj
        except IntegrityError:
            await session.rollback()
            raise EntityAlreadyExistsException(detail=f"Локация с названием '{location.name}' уже существует")
        except SQLAlchemyError:
            await session.rollback()
            raise

    async def update(
            self, 
            session: AsyncSession, 
            location_id: int, **kwargs) -> LocationModel:
        try:
            location = self.get_by_id(session, location_id)

            for key, value in kwargs.items():
                if hasattr(location, key):
                    setattr(location, key, value)

            await session.commit()
            return location
        except SQLAlchemyError:
            raise

    async def delete(self, session: AsyncSession, location_id: int) -> None:
        try:
            location = self.get_by_id(session, location_id)
            await session.delete(location)
            await session.commit()
        except SQLAlchemyError:
            raise