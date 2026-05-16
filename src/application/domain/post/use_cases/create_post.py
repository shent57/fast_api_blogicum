from datetime import datetime
import logging
from src.application.core.exceptions.database_exceptions import EntityAlreadyExistsException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.posts import PostRepository
from src.application.schemas.posts import PostRequestSchema, PostResponseSchema


logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(
        self, post: PostRequestSchema, author_id: int
    ) -> PostResponseSchema:
        try:
            async with self._database.session() as session:
                post_dict = post.model_dump()
                post_dict["author_id"] = author_id
                post_dict["created_at"] = datetime.now()
                created_post = self._post_repository.create(session, post_dict)

                return PostResponseSchema.model_validate(created_post)
        except EntityAlreadyExistsException as e:
            logger.error(e.get_detail())
            raise e