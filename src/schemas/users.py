# используется для создания моделей данных и валидации
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


class BaseUser(BaseModel):
    username: str = Field(..., max_length=150)
    bio: str = Field("", max_length=500)
    email: str = Field("", max_length=254)
    first_name: str | None = Field("", max_length=150)
    last_name: str | None = Field("", max_length=150)


class CreateUser(BaseUser):
    password: SecretStr = Field(..., min_length=8, max_length=128)

    @field_validator("username")  # валидация отдельных полей
    @staticmethod  # не требует self(не получает ссылку на экземпляр класса)
    def validate_username(username: str) -> str:
        if len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Логин должен содержать минимум 3 символа",
            )

        return username
    
    @field_validator("password")
    @staticmethod
    def validate_password(password: SecretStr) -> SecretStr:
        password_str = password.get_secret_value()
        if not any(c.isdigit() for c in password_str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать хотя бы одну цифру"
            )
        if not any(c.isupper() for c in password_str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать хотя бы одну заглавную букву"
            )
        return password


class User(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    is_active: bool
    date_joined: datetime
    id: int