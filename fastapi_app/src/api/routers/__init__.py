from .users import router as users_router
from .posts import router as posts_router
from .categories import router as categories_router
from .locations import router as locations_router

__all__ = [
    "users_router",
    "posts_router",
    "categories_router",
    "locations_router",
]