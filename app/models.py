from pydantic import BaseModel, Field, validator # используется для создания моделей данных и валидации
from datetime import datetime
from typing import Optional, List # для указания необязательных полей
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
    id: int
    is_active: bool
    date_joined: datetime
    
    class Config:
        orm_mode = True
        
        
class CategoryBase(BaseModel):
    title: str = Field(..., max_length=256, description="Заголовок категории")
    description: str = Field(..., description="Описание категории")
    slug: str = Field(..., pattern="^[-a-zA-Z0-9_]+$", description="Идентификатор категории для URL; разрешены символы латиницы, цифры, дефис и подчёркивание")
    is_published: bool = Field(True, description="Публикация категории")
    
    
@validator('slug')
def validate_slug(cls, values: str) -> str:
    if not re.match(r'^[-a-zA-Z0-9_]$', values):
        raise ValueError("Slug должен содержать только латинские буквы, цифры, дефис и подчёркивание")
    
    
    return values
    
class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class LocationBase(BaseModel):
    name: str = Field(..., max_length=256, description="Название места")
    is_published: bool = Field(True, description="Публикация места")
    
    
class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class CommentBase(BaseModel):
    text: str = Field(..., description="Текст комментария")
    is_published: bool = Field(True, description="Публикация комментария")
    
    
class CommentCreate(CommentBase):
    post_id: int
    author_id: int = Field(..., description="ID автора поста")
    
    
class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int = Field(..., description="ID автора поста")
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class PostBase(BaseModel):
    title: str = Field(..., max_length=256, description="Заголовок поста")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата и время публикации поста")
    is_published: bool = Field(True, description="Публикация поста")
    image: Optional[str] = Field(None, description="Изображение поста")
    author_id: int = Field(..., description="ID автора поста")
    category_id: int = Field(..., description="ID категории поста")
    location_id: Optional[int] = Field(None, description="Местоположение поста, может быть пустым")
    
    
@validator('pub_date')
def validate_pub_date(cls, value: datetime) -> datetime:
    if value < datetime.now():
        raise ValueError("Дата публикации не может быть в прошлом")
    return value

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    comments: List[Comment] = []
    
    class Config:
        orm_mode = True