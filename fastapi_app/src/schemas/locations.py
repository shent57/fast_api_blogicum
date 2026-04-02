from datetime import datetime

from pydantic import (  # используется для создания моделей данных и валидации
    BaseModel, Field, ConfigDict)


class LocationBase(BaseModel):
    name: str = Field(..., max_length=256, description="Название места")
    is_published: bool = Field(True, description="Публикация места")
    created_at: datetime = Field(..., description="Дата и время создания")


class LocationCreate(LocationBase):
    pass


class LocationResponseSchema(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    id: int = Field(..., description="Уникальный идентификатор места")
    model: str = Field("blog.location", description="Тип модели")


class LocationUpdateFilter(BaseModel):
    location_id: int = Field(
        ..., 
        description="Уникальный идентификатор для обновления")


class LocationUpdateData(BaseModel):
    name: str | None = Field(
        None, 
        max_length=256, 
        description="Новое название")
    is_published: bool | None = Field(
        None, 
        description="Новый статус публикаций")
    created_at: datetime | None = Field(
        None, 
        description="Новая дата создания")
