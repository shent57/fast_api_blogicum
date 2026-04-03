from fastapi import APIRouter, Depends, HTTPException, status

from api.depends import (
    create_category_use_case,
    delete_category_use_case,
    get_get_categories_use_case,
    get_get_category_by_id_use_case,
    update_category_use_case,
)
from domain.category.use_cases.create_category import CreateCategoryUseCase
from domain.category.use_cases.delete_category import DeleteCategoryUseCase
from domain.category.use_cases.get_categories import GetCategoriesUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.update_category import UpdateCategoryUseCase
from schemas.DeleteFilter import DeleteFilter
from schemas.categories import (
    CategoryCreate,
    CategoryResponseSchema,
    CategoryUpdateData,
    CategoryUpdateFilter,
)

router = APIRouter(prefix="/blogs/category", tags=["Categories"])


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