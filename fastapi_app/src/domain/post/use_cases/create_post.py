from datetime import datetime

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostRequestSchema, PostResponseSchema


class CreatePostUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(
        self, post: PostRequestSchema, author_id: int
    ) -> PostResponseSchema:
        with self._database.session() as session:
            post_dict = post.model_dump()
            post_dict["author_id"] = author_id
            post_dict["created_at"] = datetime.now()
            created_post = self._post_repository.create(session, post_dict)

            return PostResponseSchema.model_validate(created_post)