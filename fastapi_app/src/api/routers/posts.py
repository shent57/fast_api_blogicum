from fastapi import APIRouter, Depends, HTTPException, status

from api.depends import (
    create_post_use_case,
    delete_post_use_case,
    get_get_post_by_id_use_case,
    get_get_posts_use_case,
    update_post_use_case,
)
from core.exceptions.domain_exceptions import PostPermissionException
from domain.post.use_cases.create_post import CreatePostUseCase
from domain.post.use_cases.delete_post import DeletePostUseCase
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.post.use_cases.get_posts import GetPostsUseCase
from domain.post.use_cases.update_post import UpdatePostUseCase
from schemas.DeleteFilter import DeleteFilter
from schemas.posts import (
    PostRequestSchema,
    PostResponseSchema,
    PostUpdateData,
    PostUpdateFilter,
)

router = APIRouter(prefix="/blogs/post", tags=["Posts"])


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

