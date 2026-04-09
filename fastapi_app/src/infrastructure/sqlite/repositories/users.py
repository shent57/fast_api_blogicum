from typing import Type

from core.exceptions.database_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException)
from infrastructure.sqlite.models.users import User as UserModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_id(self, session: Session, user_id: int) -> UserModel:
        try:
            query = select(self._model).where(self._model.id == user_id)

            user = session.scalar(query)
            if not user:
                raise UserNotFoundException(user_id=user_id)
            return user
        except SQLAlchemyError as e:
            raise UserNotFoundException(user_id=user_id)

    def get_by_username(self, session: Session, username: str) -> UserModel:
        try:
            query = select(self._model).where(self._model.username == username)

            user = session.scalar(query)
            if not user:
                raise UserNotFoundException(username=username)
            return user
        except SQLAlchemyError as e:
            raise UserNotFoundException(username=username)

    def create(self, session: Session, user_data: dict) -> UserModel:
        query = insert(self._model).values(**user_data).returning(self._model)

        try:
            user = session.scalar(query)
            session.commit()
            return user
        except IntegrityError as e:
            session.rollback()
            raise UserAlreadyExistsException(username=user_data.get("username"))
        except SQLAlchemyError as e:
            session.rollback()
            raise UserAlreadyExistsException(username=user_data.get("username"))


    def update(self, session: Session, user_id: int, **kwargs) -> UserModel:
        try:
            user = self.get_by_id(session, user_id)

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            session.commit()
            return user
        except SQLAlchemyError as e:
            session.rollback()
            raise UserNotFoundException(user_id=user_id)

    def delete(self, session: Session, user_id: int) -> None:
        try:
            user = self.get_by_id(session, user_id)
            session.delete(user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise UserNotFoundException(user_id=user_id)
