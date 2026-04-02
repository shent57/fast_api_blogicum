from typing import List

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.posts import PostResponseSchema


class GetPostsUseCase:
    def __init__(
        self,
        post_repository: PostRepository,
        user_repository: UserRepository,
        database: Database,
    ):
        self._post_repository = post_repository
        self._user_repository = user_repository
        self._database = database

    async def execute(
        self,
        category_id: int | None = None,
        author: int | None = None,
        location: int | None = None,
    ) -> List[PostResponseSchema]:
        with self._database.session() as session:
            posts = self._post_repository.get_all(session)

            if category_id is not None:
                posts = [p for p in posts if p.category_id == category_id]

            if author is not None:
                posts = [p for p in posts if p.author_id == author]
            if location is not None:
                posts = [p for p in posts if p.location_id == location]

            return [PostResponseSchema.model_validate(post) for post in posts]