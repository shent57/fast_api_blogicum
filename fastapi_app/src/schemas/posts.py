from pydantic import BaseModel, Field # используется для создания моделей данных и валидации
from datetime import datetime
from typing import List # для указания необязательных полей

class PostRequestSchema(BaseModel):
    text: str = Field(..., max_length=80)
    author: int
    title: str = Field(..., max_length=256)
    pub_date: datetime
    is_published: bool = True
    image: str | None = None
    category: int
    location: int | None = None

class PostResponseSchema(BaseModel):
    post_text: str
    author_name: str
    title: str
    pub_date: datetime
    is_published: bool
    image: str | None = None
    category: int
    location: int | None = None
    pk: int
    comments: List['CommentResponseSchema'] = []
        
        
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