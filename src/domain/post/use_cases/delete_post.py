from src.core.exceptions.domain_exceptions import PostPermissionException
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.infrastructure.sqlite.database import Database
from src.infrastructure.sqlite.repositories.posts import PostRepository
import logging

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(
            self, 
            post_id: int, 
            user_id: int, 
            is_staff: bool = False) -> None:
        try:
            with self._database.session() as session:
                self._post_repository.delete(
                    session, 
                    post_id, 
                    user_id, 
                    is_staff)
        except PermissionError:
            error = PostPermissionException("удаления")
            logger.error(error.get_detail())
            raise error
        except PostNotFoundException as e:
            logger.error(e.get_detail())
            raise e