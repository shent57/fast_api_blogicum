from api.depends import (create_category_use_case, create_location_use_case,
                         create_post_use_case, create_user_use_case,
                         delete_category_use_case, delete_location_use_case,
                         delete_post_use_case, get_get_categories_use_case,
                         get_get_category_by_id_use_case,
                         get_get_location_by_id_use_case,
                         get_get_locations_use_case,
                         get_get_post_by_id_use_case, get_get_posts_use_case,
                         get_get_user_by_login_use_case,
                         update_category_use_case, update_location_use_case,
                         update_post_use_case)
from core.exceptions.domain_exceptions import (PostPermissionException,
                                               UserLoginIsNotUniqueException,
                                               UserNotFoundByLoginException)
from domain.category.use_cases.create_category import CreateCategoryUseCase
from domain.category.use_cases.delete_category import DeleteCategoryUseCase
from domain.category.use_cases.get_categories import GetCategoriesUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.update_category import UpdateCategoryUseCase
from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase
from domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from domain.location.use_cases.get_locations import GetLocationsUseCase
from domain.location.use_cases.update_location import UpdateLocationUseCase
from domain.post.use_cases.create_post import CreatePostUseCase
from domain.post.use_cases.delete_post import DeletePostUseCase
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.post.use_cases.get_posts import GetPostsUseCase
from domain.post.use_cases.update_post import UpdatePostUseCase
from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.categories import (CategoryCreate, CategoryResponseSchema,
                                CategoryUpdateData, CategoryUpdateFilter)
from schemas.DeleteFilter import DeleteFilter
from schemas.locations import (LocationCreate, LocationResponseSchema,
                               LocationUpdateData, LocationUpdateFilter)
from schemas.posts import (PostRequestSchema, PostResponseSchema,
                           PostUpdateData, PostUpdateFilter)
from schemas.users import CreateUser, User

router = APIRouter()


@router.get(
        "/user/{login}", 
        status_code=status.HTTP_200_OK, 
        response_model=User)
async def get_user_by_login(
    login: str,
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
) -> User:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: CreateUser,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> User:
    try:
        return await use_case.execute(user=user)
    except UserLoginIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )


@router.get("/blogs/post/{post_id}", response_model=PostResponseSchema)
async def get_posts_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
) -> PostResponseSchema:
    return await use_case.execute(post_id)


@router.get("/blogs/post", response_model=list[PostResponseSchema])
async def get_posts(
    category_id: int | None = None,
    author: int | None = None,
    location: int | None = None,
    use_case: GetPostsUseCase = Depends(get_get_posts_use_case),
) -> list[PostResponseSchema]:
    return await use_case.execute(category_id, author, location)


@router.post(
    "/blogs/post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
)
async def create_post(
    post: PostRequestSchema,
    current_user_id: int = 1,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponseSchema:
    return await use_case.execute(post, current_user_id)


@router.put(
    "/blogs/post/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchema,
)
async def update_post(
    filter_post: PostUpdateFilter,
    new_data: PostUpdateData,
    current_user_id: int = 1,
    is_stuff: bool = False,  # флаг админа
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(
            filter_post.post_id, current_user_id, new_data, is_stuff
        )
    except PostPermissionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )


@router.delete("/blogs/post", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    delete_filter: DeleteFilter,
    current_user_id: int = 1,
    is_staff: bool = False,
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
) -> None:
    if delete_filter.key != "pk":
        raise HTTPException(
            status_code=400, 
            detail="Можно удалять только по pk")

    try:
        await use_case.execute(delete_filter.value, current_user_id, is_staff)
    except PostPermissionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )

    return


@router.get(
        "/blogs/category/{category_id}", 
        response_model=CategoryResponseSchema)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(
        get_get_category_by_id_use_case),
) -> CategoryResponseSchema:
    return await use_case.execute(category_id)


@router.get("/blogs/category", response_model=list[CategoryResponseSchema])
async def get_categories(
    is_published: bool | None = None,
    title: str | None = None,
    use_case: GetCategoriesUseCase = Depends(get_get_categories_use_case),
) -> list[CategoryResponseSchema]:
    return await use_case.execute(is_published, title)


@router.post(
    "/blogs/category",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponseSchema,
)
async def create_category(
    category: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponseSchema:
    return await use_case.execute(category)


@router.put(
    "/blogs/category",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponseSchema,
)
async def update_category(
    filter_category: CategoryUpdateFilter,
    new_data: CategoryUpdateData,
    use_case: UpdateCategoryUseCase = Depends(update_category_use_case),
) -> CategoryResponseSchema:
    return await use_case.execute(filter_category.category_id, new_data)


@router.delete("/blogs/category", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    delete_filter: DeleteFilter,
    use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
) -> None:
    if delete_filter.key != "pk":
        raise HTTPException(
            status_code=400, 
            detail="Можно удалять только по pk")

    await use_case.execute(delete_filter.value)
    return


@router.get(
        "/blogs/location/{location_id}", 
        response_model=LocationResponseSchema)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(
        get_get_location_by_id_use_case),
) -> LocationResponseSchema:
    return await use_case.execute(location_id)


@router.get("/blogs/location", response_model=list[LocationResponseSchema])
async def get_locations(
    is_published: bool = True,
    name: str | None = None,
    use_case: GetLocationsUseCase = Depends(get_get_locations_use_case),
) -> list[LocationResponseSchema]:
    return await use_case.execute(is_published, name)


@router.post(
    "/blogs/location",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationResponseSchema,
)
async def create_location(
    location: LocationCreate,
    use_case: CreateLocationUseCase = Depends(create_location_use_case),
) -> LocationResponseSchema:
    return await use_case.execute(location)


@router.put(
    "/blogs/location",
    status_code=status.HTTP_200_OK,
    response_model=LocationResponseSchema,
)
async def update_location(
    filter_location: LocationUpdateFilter,
    new_data: LocationUpdateData,
    use_case: UpdateLocationUseCase = Depends(update_location_use_case),
) -> LocationResponseSchema:
    return await use_case.execute(filter_location.location_id, new_data)


@router.delete("/blogs/location", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    delete_filter: DeleteFilter,
    use_case: DeleteLocationUseCase = Depends(delete_location_use_case),
) -> None:
    if delete_filter.key != "pk":
        raise HTTPException(
            status_code=400, 
            detail="Можно удалять только по pk")

    await use_case.execute(delete_filter.value)
    return
