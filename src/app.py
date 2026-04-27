from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api.routers import (
    categories_router,
    locations_router,
    posts_router,
    users_router,
)

from src.api.base import router as base_router
from src.api.auth import router as auth_router
from src.api.auth import router as auth_router
from src.api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    # Нужно добавить обязательно:
    app.add_middleware(
        CORSMiddleware,
        # с каких приложений можно запускать, * - все приложения
        allow_origins=["*"],
        # разрешаем аутентификацию, иначе авторизация недоступна
        allow_credentials=True,  # разрешены куки и авторизация
        allow_methods=["*"],  # разрешены все методы
        allow_headers=["*"],  # разрешены все заголовки
    )

    # Подключаем роутер с энпоинтами
    app.include_router(posts_router, prefix="/posts", tags=["Posts"])
    app.include_router(locations_router, prefix="/locations", tags=["Locations"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(categories_router, prefix="/categories", tags=["Categories"])
    app.include_router(base_router, prefix="/base", tags=["Base APIs"])
    app.include_router(auth_router, tags=["Auth"])
    return app
