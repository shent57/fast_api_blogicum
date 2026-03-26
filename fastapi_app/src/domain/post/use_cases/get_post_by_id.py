from core.exceptions.database_exceptions import PostNotFoundException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema


class GetPostByIdUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(self, post_id: int) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._post_repository.get_by_id(session, post_id)
            if not post:
                raise PostNotFoundException()

            return PostResponseSchema(
                post_text=post.text,
                author_name="",
                title=post.title,
                pub_date=post.pub_date,
                is_published=post.is_published,
                image=post.image,
                category=post.category_id,
                location=post.location_id,
                pk=post.id,
                comments=[],
            )
