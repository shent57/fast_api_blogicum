from core.exceptions.domain_exceptions import PostPermissionException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.posts import PostRepository


class DeletePostUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(
            self, 
            post_id: int, 
            user_id: int, 
            is_staff: bool = False) -> None:
        with self._database.session() as session:
            try:
                self._post_repository.delete(
                    session, 
                    post_id, 
                    user_id, 
                    is_staff)
            except PermissionError:
                raise PostPermissionException("удаления")
