from datetime import datetime

from core.exceptions.database_exceptions import UserAlreadyExistsException
from core.exceptions.domain_exceptions import UserLoginIsNotUniqueException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import CreateUser
from schemas.users import User as UserSchema


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, database: Database):
        self._database = database
        self._user_repository = user_repository

    async def execute(self, user: CreateUser) -> UserSchema:
        try:
            with self._database.session() as session:
                user_dict = user.model_dump()
                user_dict["password"] = user.password.get_secret_value()
                user_dict["date_joined"] = datetime.now()
                user_dict["last_login"] = None
                created_user = self._user_repository.create(session, user_dict)
        except UserAlreadyExistsException:
            raise UserLoginIsNotUniqueException(login=user.username)

        date_joined = (
            created_user.date_joined
            if isinstance(created_user.date_joined, datetime)
            else datetime.fromisoformat(created_user.date_joined)
        )

        return UserSchema(
            username=created_user.username,
            bio=created_user.bio,
            email=created_user.email,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            is_active=created_user.is_active,
            date_joined=date_joined,
            pk=created_user.id,
        )
