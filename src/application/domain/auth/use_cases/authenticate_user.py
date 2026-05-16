import logging

from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.users import UserRepository
from src.application.schemas.users import User as UserSchema
from src.application.resources.auth import verify_password
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.core.exceptions.domain_exceptions import UserNotFoundByLoginException, WrongPasswordException

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()


    async def execute(
        self,
        login: str,
        password: str,
    ) -> UserSchema:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_by_username(session=session, username=login)
        except EntityNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(error.get_detail())
            raise error

        if not verify_password(plain_password=password, hashed_password=user.password):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserSchema.model_validate(obj=user)