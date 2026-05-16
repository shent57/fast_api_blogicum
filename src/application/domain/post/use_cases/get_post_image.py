from fastapi.responses import FileResponse

from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.posts import PostRepository
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.core.exceptions.domain_exceptions import PostNotFoundException, PostHasNotImageException


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()
        self._database = database
        self.image_folder = "./../images"


    async def execute(self, post_id: int) -> FileResponse:
        try:
            async with self._database.session() as session:
                post = await self._repo.get(session=session, id=post_id)
        except EntityNotFoundException:
            raise PostNotFoundException(post_id=post_id)
        
        if not post.image_path:
            raise PostHasNotImageException()
        
        full_image_path: str = f"{self.image_folder}/{post.image_path}.jpeg"
        return FileResponse(full_image_path, media_type="image/jpeg")