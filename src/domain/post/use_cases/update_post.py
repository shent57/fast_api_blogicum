from src.core.exceptions.domain_exceptions import PostPermissionException
from src.infrastructure.sqlite.database import Database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.posts import PostResponseSchema, PostUpdateData
import logging

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(
        self,
        post_id: int,
        user_id: int,
        post_data: PostUpdateData,
        is_staff: bool = False,
    ) -> PostResponseSchema:
        try:
            with self._database.session() as session:
                updated_post = self._post_repository.update(
                    session, post_id, user_id, post_data, is_staff
                )
        except PermissionError:
            error = PostPermissionException("редактирования")
            logger.error(error.get_detail())
            raise error

        return PostResponseSchema.model_validate(updated_post)