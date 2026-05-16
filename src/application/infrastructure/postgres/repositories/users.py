from typing import Type

from src.application.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException)
from src.application.infrastructure.postgres.models.users import User as UserModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    async def get_by_id(self, session: AsyncSession, user_id: int) -> UserModel:
            query = select(self._model).where(self._model.id == user_id)

            user = await session.scalar(query)
            if not user:
                raise EntityNotFoundException(
                    detail=f"Пользователь с id={user_id} не найден"
                )
            return user

    async def get_by_username(self, session: AsyncSession, username: str) -> UserModel:
            query = select(self._model).where(self._model.username == username)

            user = await session.scalar(query)
            if not user:
                raise EntityNotFoundException(
                    detail=f"Пользователь с логином {username} не найден"
                )
            return user

    async def create(self, session: AsyncSession, user_data: dict) -> UserModel:
        query = insert(self._model).values(**user_data).returning(self._model)
        
        try:
            user = await session.scalar(query)
            await session.commit()
            return user
        except IntegrityError:
            await session.rollback()
            raise EntityAlreadyExistsException(detail=f"Пользователь с логином {user_data.get('username')} уже существует")


    async def update(self, session: AsyncSession, user_id: int, **kwargs) -> UserModel:
            user = self.get_by_id(session, user_id)

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            await session.commit()
            return user

    async def delete(self, session: AsyncSession, user_id: int) -> None:
            user = self.get_by_id(session, user_id)
            await session.delete(user)
            await session.commit()