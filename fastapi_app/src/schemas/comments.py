from pydantic import BaseModel, Field # используется для создания моделей данных и валидации
from datetime import datetime


class CommentBase(BaseModel):
    text: str = Field(..., description="Текст комментария")
    is_published: bool = Field(True, description="Публикация комментария")
    created_at: datetime = Field(..., description="Дата и время создания")
    
    
class CommentCreate(CommentBase):
    post_id: int = Field(..., description="ID поста")
    author_id: int = Field(..., description="ID автора комментария")
    
    
class CommentResponseSchema(CommentBase):
    post_id: int = Field(..., description="ID поста")
    author_id: int = Field(..., description="ID автора комментария")
    model: str = 'blog.comment'
    id: int = Field(..., description="Уникальный идентификатор комментария")


class CommentUpdateFilter(BaseModel):
    comment_id: int = Field(..., description="Уникальный идентификатор для обновления")


class CommentUpdateData(BaseModel):
    text: str | None = Field(None, description="Новый текст комментария")
    is_published: bool | None = Field(None, description="Новый статус публикации")