from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase
from src.domain.category.use_cases.get_categories import GetCategoriesUseCase
from src.domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase
from src.domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from src.domain.location.use_cases.get_locations import GetLocationsUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from src.domain.post.use_cases.get_posts import GetPostsUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_post_repository() -> PostRepository:
    return PostRepository()


def get_category_repository() -> CategoryRepository:
    return CategoryRepository()


def get_location_repository() -> LocationRepository:
    return LocationRepository()


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase(
        user_repository=get_user_repository(), database=database
    )


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository=get_user_repository(), 
        database=database)


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def get_get_posts_use_case() -> GetPostsUseCase:
    return GetPostsUseCase(
        post_repository=get_post_repository(),
        user_repository=get_user_repository(),
        database=database,
    )


def get_get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase(
        post_repository=get_post_repository(), 
        database=database)


def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase(
        post_repository=get_post_repository(), 
        database=database)


def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase(
        post_repository=get_post_repository(), 
        database=database)


def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase(
        post_repository=get_post_repository(), 
        database=database)


def get_get_locations_use_case() -> GetLocationsUseCase:
    return GetLocationsUseCase(
        location_repository=get_location_repository(), database=database
    )


def get_get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase(
        location_repository=get_location_repository(), database=database
    )


def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase(
        location_repository=get_location_repository(), database=database
    )


def update_location_use_case() -> UpdateLocationUseCase:
    return UpdateLocationUseCase(
        location_repository=get_location_repository(), database=database
    )


def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase(
        location_repository=get_location_repository(), database=database
    )


def get_get_categories_use_case() -> GetCategoriesUseCase:
    return GetCategoriesUseCase(
        category_repository=get_category_repository(), database=database
    )


def get_get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase(
        category_repository=get_category_repository(), database=database
    )


def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase(
        category_repository=get_category_repository(), database=database
    )


def update_category_use_case() -> UpdateCategoryUseCase:

    return UpdateCategoryUseCase(
        category_repository=get_category_repository(), database=database
    )


def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase(
        category_repository=get_category_repository(), database=database
    )

