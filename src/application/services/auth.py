from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt

from src.application.core.exceptions.auth_exceptions import CredentialsException
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.schemas.users import User as UserSchema
from src.application.resources.auth import oauth2_scheme
from src.application.infrastructure.postgres.database import database as postgres_database, Database
from src.application.infrastructure.postgres.repositories.users import UserRepository
from src.application.core.config import settings


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        _AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
        _database: Database = postgres_database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[settings.AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)

        try:
            async with _database.session() as session:
                user = await _repo.get_by_username(session=session, username=username)
        except EntityNotFoundException:
            raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)

        return UserSchema.model_validate(obj=user)