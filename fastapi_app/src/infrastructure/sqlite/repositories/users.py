from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.models.users import User as UserModel
from schemas.users import UserCreate as UserSchema
from core.exceptions.database_exceptions import UserNotFoundException, UserAlreadyExistsException


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_id(self, session: Session, user_id: int) -> UserModel:
        query = (
            select(self._model)
            .where(self._model.id == user_id)
        )

        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()

        return user
    
    def get_by_username(self, session: Session, username: str) -> UserModel:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )

        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()

        return user
    
    def create(self, session: Session, user: UserSchema) -> UserModel:
        query = (
            insert(self._model)
            .values(**user.model_dump())
            .returning(self._model)
        )

        try:
            user = session.scalar(query)
        except IntegrityError:
            raise UserAlreadyExistsException()

        return user

    def update(self, session: Session, user_id: int, **kwargs) -> UserModel:
        user = self.get_by_id(session, user_id)

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        session.commit()

        return user
    
    def delete(self, session: Session, user_id: int) -> None:
        user = self.get_by_id(session, user_id)
        session.delete(user)