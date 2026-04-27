import logging
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.infrastructure.sqlite.database import Database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User as UserSchema

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self, user_repository: UserRepository, database: Database):
        self._database = database
        self._user_repository = user_repository

    async def execute(self, login: str, current_user: UserSchema) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._user_repository.get_by_username(session, login)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(
                f"Пользователь {current_user.username} довел приложение до ошибки: {error.get_detail()}"
            )
            raise error

        return UserSchema.model_validate(user)