from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from fastapi.responses import FileResponse

from src.application.services.auth import AuthService

from src.application.api.depends import (
    create_post_use_case,
    delete_post_use_case,
    get_get_post_by_id_use_case,
    get_get_posts_use_case,
    update_post_use_case,
    get_post_image_use_case,
    add_post_image_use_case,
)
from src.application.core.exceptions.domain_exceptions import PostPermissionException
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.domain.post.use_cases.create_post import CreatePostUseCase
from src.application.domain.post.use_cases.delete_post import DeletePostUseCase
from src.application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from src.application.domain.post.use_cases.get_posts import GetPostsUseCase
from src.application.domain.post.use_cases.update_post import UpdatePostUseCase
from src.application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from src.application.domain.post.use_cases.get_post_image import GetPostImageUseCase
from src.application.domain.post.use_cases.delete_post import DeletePostUseCase
from src.application.schemas.DeleteFilter import DeleteFilter
from src.application.schemas.posts import (
    PostRequestSchema,
    PostResponseSchema,
    PostUpdateData,
    PostUpdateFilter,
    PostImageResponse,
)


router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@router.get("/blogs/post/{post_id}", response_model=PostResponseSchema)
async def get_posts_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(post_id)
    except EntityNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


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
    is_stuff: bool = False,
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


@router.get("/image/post/{post_id}", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def get_post_image(
    post_id: int,
    use_case: GetPostImageUseCase = Depends(get_post_image_use_case),
) -> FileResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except (EntityNotFoundException,) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post("/image/post", status_code=status.HTTP_200_OK, response_model=PostImageResponse)
async def add_post_image(
    image: UploadFile = File(...),
    use_case: AddPostImageUseCase = Depends(add_post_image_use_case),
) -> PostImageResponse:
    return await use_case.execute(image=image)

