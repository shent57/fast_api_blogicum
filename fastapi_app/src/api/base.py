from fastapi import APIRouter

from api.routers import (
    users_router,
    posts_router,
    categories_router,
    locations_router,
)

router = APIRouter()

# Подключаем все роутеры
router.include_router(users_router)
router.include_router(posts_router)
router.include_router(categories_router)
router.include_router(locations_router)