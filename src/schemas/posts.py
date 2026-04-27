from datetime import datetime
from typing import List  # для указания необязательных полей
from fastapi import HTTPException, status
from pydantic import (  # используется для создания моделей данных и валидации
    BaseModel, 
    Field, 
    ConfigDict,
    field_validator)
from src.schemas.comments import CommentResponseSchema


class PostRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(..., max_length=80)
    title: str = Field(..., max_length=256)
    pub_date: datetime
    is_published: bool = True
    created_at: datetime
    image: str | None = None
    category_id: int
    location_id: int | None = None

    @field_validator("pub_date")
    @staticmethod
    def validate_pub_date(pub_date: datetime) -> datetime:
        if pub_date < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Дата публикации не может быть в прошлом",
            )
        return pub_date
    
    @field_validator("title")
    @staticmethod
    def validate_title(title: str) -> str:
        if not title or title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Заголовок не может быть пустым",
            )
        return title.strip()


class PostResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    author_name: str
    title: str
    pub_date: datetime
    is_published: bool
    image: str | None = None
    category_id: int
    location_id: int | None = None
    id: int
    comments: List["CommentResponseSchema"] = []


class PostUpdateFilter(BaseModel):
    post_id: int


class PostUpdateData(BaseModel):
    title: str | None = Field(None, max_length=256)
    text: str | None = None
    pub_date: datetime | None = None
    is_published: bool | None = None
    image: str | None = None
    author: int | None = None
    category: int | None = None
    location: int | None = None
    created_at: datetime | None = None

    @field_validator("title")
    @staticmethod
    def validate_title(title: str | None) -> str | None:
        if title is not None and not title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Заголовок не может быть пустым",
            )
        return title.strip() if title else None