from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.base import router as base_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1") 
# Нужно добавить обязательно: 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # с каких приложений можно запускать, * - все приложения
        allow_credentials=True,  # разрешаем аутентификацию, иначе авторизация недоступна
        allow_methods=["*"],   # можно вызывать только POST-методы
        allow_headers=["*"],  
    ) 
    
    app.include_router(base_router, prefix="/base", tags=["Base APIs"])

    return app
