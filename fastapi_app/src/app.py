from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api.routers import (
    categories_router,
    locations_router,
    posts_router,
    users_router,
)


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
    app.include_router(posts_router)
    app.include_router(locations_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    return app
