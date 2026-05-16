from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.application.api.routers import (
    categories_router,
    locations_router,
    posts_router,
    users_router,
)
from src.application.api.base import router as base_router
from src.application.api.auth import router as auth_router
from src.application.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_PATH)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS.split(",") if settings.ORIGINS else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(posts_router, prefix="/posts", tags=["Posts"])
    app.include_router(locations_router, prefix="/locations", tags=["Locations"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(categories_router, prefix="/categories", tags=["Categories"])
    app.include_router(base_router, prefix="/base", tags=["Base APIs"])
    app.include_router(auth_router, tags=["Auth"])

    return app

