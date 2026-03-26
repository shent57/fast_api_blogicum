from core.exceptions.domain_exceptions import PostPermissionException
from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema, PostUpdateData


class UpdatePostUseCase:
    def __init__(self, post_repository: PostRepository, database: Database):
        self._post_repository = post_repository
        self._database = database

    async def execute(
        self,
        post_id: int,
        user_id: int,
        post_data: PostUpdateData,
        is_stuff: bool = False,
    ) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                updated_post = self._post_repository.update(
                    session, post_id, user_id, post_data, is_stuff
                )
            except PermissionError:
                raise PostPermissionException("редактирования")

            return PostResponseSchema(
                post_text=updated_post.text,
                author_name="",
                title=updated_post.title,
                pub_date=updated_post.pub_date,
                is_published=updated_post.is_published,
                image=updated_post.image,
                category=updated_post.category_id,
                location=updated_post.location_id,
                pk=updated_post.id,
                comments=[],
            )
