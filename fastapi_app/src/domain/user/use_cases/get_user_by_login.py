from datetime import datetime

from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByLoginException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema


class GetUserByLoginUseCase:
    def __init__(self, user_repository: UserRepository, database: Database):
        self._database = database
        self._user_repository = user_repository

    async def execute(self, login: str) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._user_repository.get_by_username(session, login)
        except UserNotFoundException:
            raise UserNotFoundByLoginException(login=login)

        return UserSchema.model_validate(user)