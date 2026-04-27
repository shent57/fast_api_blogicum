from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_category_use_case,
    delete_category_use_case,
    get_get_categories_use_case,
    get_get_category_by_id_use_case,
    update_category_use_case,
)
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase
from src.domain.category.use_cases.get_categories import GetCategoriesUseCase
from src.domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.schemas.DeleteFilter import DeleteFilter
from src.schemas.categories import (
    CategoryCreate,
    CategoryResponseSchema,
    CategoryUpdateData,
    CategoryUpdateFilter,
)

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException, 
    CategoryAlreadyExistsException)

router = APIRouter(prefix="/blogs/category", tags=["Categories"])


@router.get(
        "/blogs/category/{category_id}", 
        response_model=CategoryResponseSchema)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(
        get_get_category_by_id_use_case),
) -> CategoryResponseSchema:
    try:
        return await use_case.execute(category_id)
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.get("/blogs/category", response_model=list[CategoryResponseSchema])
async def get_categories(
    is_published: bool | None = None,
    title: str | None = None,
    use_case: GetCategoriesUseCase = Depends(get_get_categories_use_case),
) -> list[CategoryResponseSchema]:
    try:
        return await use_case.execute(is_published, title)
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post(
    "/blogs/category",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponseSchema,
)
async def create_category(
    category: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponseSchema:
    try:
        return await use_case.execute(category)
    except CategoryAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
    )


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
    try:
        return await use_case.execute(filter_category.category_id, new_data)
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.delete("/blogs/category", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    delete_filter: DeleteFilter,
    use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
) -> None:
    if delete_filter.key != "pk":
        raise HTTPException(
            status_code=400, 
            detail="Можно удалять только по pk")
    try:
        await use_case.execute(delete_filter.value)
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )