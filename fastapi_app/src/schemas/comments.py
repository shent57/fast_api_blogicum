from datetime import datetime
from fastapi import HTTPException, status
from pydantic import (  # используется для создания моделей данных и валидации
    BaseModel, Field, ConfigDict, field_validator)


class CommentBase(BaseModel):
    text: str = Field(..., description="Текст комментария")
    is_published: bool = Field(True, description="Публикация комментария")
    created_at: datetime = Field(..., description="Дата и время создания")

    @field_validator("text")
    @staticmethod
    def validate_text(text: str) -> str:
        if not text or not text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Текст комментария не может быть пустым",
            )
        return text.strip()


class CommentCreate(CommentBase):
    post_id: int = Field(..., description="ID поста")
    author_id: int = Field(..., description="ID автора комментария")


class CommentResponseSchema(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    post_id: int = Field(..., description="ID поста")
    author_id: int = Field(..., description="ID автора комментария")
    model: str = "blog.comment"
    id: int = Field(..., description="Уникальный идентификатор комментария")


class CommentUpdateFilter(BaseModel):
    comment_id: int = Field(
        ..., 
        description="Уникальный идентификатор для обновления")


class CommentUpdateData(BaseModel):
    text: str | None = Field(None, description="Новый текст комментария")
    is_published: bool | None = Field(
        None, 
        description="Новый статус публикации")
    
    @field_validator("text")
    @staticmethod
    def validate_text(text: str | None) -> str | None:
        if text is not None and not text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Текст комментария не может быть пустым",
            )
        return text.strip() if text else None