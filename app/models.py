from pydantic import BaseModel, Field, validator # используется для создания моделей данных и валидации
from datetime import datetime, timezone
from typing import Optional, List, Any # для указания необязательных полей
import re # для использования регулярных выражений 

class UserBase(BaseModel):
    username: str = Field(
        ...,
        description="Логин пользователя, от 1 до 150 символов",
        max_length=150)
    bio: Optional[str] = Field(None, description="Биография пользователя")
    email: Optional[str] = Field(None, description="Email пользователя")
    first_name: Optional[str] = Field(None, max_length=150, description="Имя пользователя")
    last_name: Optional[str] = Field(None, max_length=150, description="Фамилия пользователя")
    
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Пароль пользователя, должен содержать как минимум 8 символов")
    

 
class User(UserBase):
    is_active: bool
    date_joined: datetime
    model: str = 'auth.user'
    pk: int
    
    class Config:
        orm_mode = True
        
class CategoryFields(BaseModel):
    title: str = Field(..., max_length=256)
    description: str = Field(...)
    slug: str = Field(..., pattern="^[-a-zA-Z0-9_]+$")
    is_published: bool = Field(True)
    created_at: datetime
    
    @validator('slug')
    def validate_slug(cls, v: str) -> str:
        if not re.match(r'^[-a-zA-Z0-9_]+$', v):
            raise ValueError("Slug должен содержать только латинские буквы, цифры, дефис и подчёркивание")
        return v
    
class CategoryCreate(CategoryFields):
    pass

class Category(BaseModel):
    model: str = "blog.category"
    pk: int
    fields: CategoryFields
    
    class Config:
        orm_mode = True
        
class CategoryUpdateFilter(BaseModel):
    category_id: int

    
class CategoryUpdateData(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None
    
    
class LocationFields(BaseModel):
    name: str = Field(..., max_length=256, description="Название места")
    is_published: bool = Field(True, description="Публикация места")
    created_at: datetime
    
    
class LocationCreate(LocationFields):
    pass


class Location(BaseModel):
    model: str = "blog.location"
    pk: int
    fields: LocationFields
    
    class Config:
        orm_mode = True
        
class LocationUpdateFilter(BaseModel):
    location_id: int
    
class LocationUpdateData(BaseModel):
    fields: Optional[LocationFields] = None
        
        
class CommentBase(BaseModel):
    text: str = Field(..., description="Текст комментария")
    is_published: bool = Field(True, description="Публикация комментария")
    created_at: datetime
    
    
class CommentCreate(CommentBase):
    post_id: int
    author: int = Field(..., description="ID автора поста")
    
    
class Comment(CommentBase):
    post_id: int
    author: int = Field(..., description="ID автора поста")
    model: str = 'blog.comment'
    pk: int
    
    class Config:
        orm_mode = True
        
        
class PostBase(BaseModel):
    title: str = Field(..., max_length=256, description="Заголовок поста")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата и время публикации")
    is_published: bool = Field(True, description="Публикация поста")
    image: Optional[str] = Field(None, description="Изображение поста")
    author: int = Field(..., description="ID автора поста")
    category: int = Field(..., description="ID категории поста")
    location: Optional[int] = Field(None, description="Местоположение поста, может быть пустым")
    created_at: datetime

class PostCreate(PostBase):
    pass

class Post(PostBase):
    model: str = "blog.post"
    pk: int
    comments: List[Comment] = []
    
    class Config:
        orm_mode = True
        
        
class PostUpdateFilter(BaseModel):
    post_id: int
    
class PostUpdateData(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    image: Optional[str] = None
    author: Optional[int] = None
    category: Optional[int] = None
    location: Optional[int] = None
    created_at: Optional[datetime] = None
    


class DeleteFilter(BaseModel):
    key: str
    value: Any