from core.exceptions.database_exceptions import PostNotFoundException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema
import logging

logger = logging.getLogger(__name__)


class GetPostByIdUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(self, post_id: int) -> PostResponseSchema:
        try:
            with self._database.session() as session:
                post = self._post_repository.get_by_id(session, post_id)
                return PostResponseSchema.model_validate(post)
        except PostNotFoundException as e:
            logger.error(e.get_detail())
            raise e