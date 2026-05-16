import re  # для использования регулярных выражений
from datetime import datetime
from fastapi import HTTPException, status
from pydantic import (  # используется для создания моделей данных и валидации
    BaseModel, Field, field_validator, ConfigDict)


class CategoryBase(BaseModel):
    title: str = Field(..., max_length=256, description="Заголовок категории")
    description: str = Field(..., description="Описание категории")
    slug: str = Field(
        ..., pattern="^[-a-zA-Z0-9_]+$", 
        description="Уникальный идентификатор для URL"
    )
    is_published: bool = Field(True, description="Публикация категории")
    created_at: datetime = Field(..., description="Дата и время создания")

    @field_validator("slug")
    @staticmethod
    def validate_slug(slug: str) -> str:
        if not re.match(r"^[-a-zA-Z0-9_]+$", slug):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Slug должен содержать только латинские буквы, цифры, дефис и подчёркивание"
            )
        return slug


class CategoryCreate(CategoryBase):
    pass


class CategoryResponseSchema(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    id: int = Field(..., description="Уникальный идентификатор категории")
    model: str = Field("blog.category", description="Тип модели")


class CategoryUpdateFilter(BaseModel):
    category_id: int = Field(
        ..., 
        description="Уникальный идентификатор для обновления")


class CategoryUpdateData(BaseModel):
    title: str | None = Field(None, max_length=256)
    description: str | None = None
    slug: str | None = None
    is_published: bool | None = None
    created_at: datetime | None = None
