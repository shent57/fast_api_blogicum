from datetime import datetime

from src.core.exceptions.database_exceptions import UserAlreadyExistsException
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException
from src.infrastructure.sqlite.database import Database
from src.resources.auth import get_password_hash
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import CreateUser
from src.schemas.users import User as UserSchema
import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, database: Database):
        self._database = database
        self._user_repository = user_repository

    async def execute(self, user: CreateUser) -> UserSchema:
        try:
            with self._database.session() as session:
                user_dict = user.model_dump()
                user_dict["password"] = get_password_hash(password=user.password.get_secret_value())
                user_dict["date_joined"] = datetime.now()
                user_dict["last_login"] = None
                created_user = self._user_repository.create(session, user_dict)
        except UserAlreadyExistsException:
            error = UserLoginIsNotUniqueException(login=user.username)
            logger.error(error.get_detail())
            raise error

        return UserSchema.model_validate(created_user)