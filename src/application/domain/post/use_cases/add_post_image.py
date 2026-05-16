from uuid import uuid4
import shutil

from fastapi import File

from src.application.schemas.posts import PostImageResponse
from src.application.core.exceptions.domain_exceptions import UploadFileIsNotImageException


class AddPostImageUseCase:
    def __init__(self) -> None:
        self.image_folder = "./../images"


    async def execute(self, image: File) -> PostImageResponse:
        if image.filename.split(".")[-1] != "jpeg":
            raise UploadFileIsNotImageException()
        
        new_image_name: str = str(uuid4())
        new_image_path: str = f"{self.image_folder}/{new_image_name}.jpeg"

        with open(new_image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        return PostImageResponse(image_path=new_image_path)