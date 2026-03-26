from api.base import router as base_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


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
    app.include_router(base_router, prefix="/base", tags=["Base APIs"])

    return app
