from pydantic import BaseModel, SecretStr, ConfigDict, field_validator, Field # используется для создания моделей данных и валидации
from datetime import datetime
from typing import Optional 
from fastapi import HTTPException, status


class BaseUser(BaseModel):
    username: str = Field(..., max_length=150)
    bio: str | None = None # биография
    email: str | None = None
    first_name: str | None = Field(None, max_length=150)
    last_name: str | None = Field(None, max_length=150)


class UserCreate(BaseUser):
    password: SecretStr = Field(..., min_length=8)

    @field_validator("username") # валидация отдельных полей
    @staticmethod # не требует self(не получает ссылку на экземпляр класса)
    def validate_username(username: str) -> str:
        if len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Логин должен содержать минимум 3 символа"
            )
        
        return username
    

    @field_validator("password")
    @staticmethod
    def validate_password(password: SecretStr) -> SecretStr:
        password_str = password.get_secret_value() # Извлекаем реальное значение пароля
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
    

class UserResponseSchema(BaseUser):

    username: str
    is_active: bool
    date_joined: datetime
    model: str = 'auth.user'
    pk: int
    bio: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None