from fastapi import APIRouter, Depends, HTTPException, status

from api.depends import (
    create_location_use_case,
    delete_location_use_case,
    get_get_location_by_id_use_case,
    get_get_locations_use_case,
    update_location_use_case,
)
from core.exceptions.database_exceptions import LocationNotFoundException
from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase
from domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from domain.location.use_cases.get_locations import GetLocationsUseCase
from domain.location.use_cases.update_location import UpdateLocationUseCase
from schemas.DeleteFilter import DeleteFilter
from schemas.locations import (
    LocationCreate,
    LocationResponseSchema,
    LocationUpdateData,
    LocationUpdateFilter,
)

router = APIRouter(prefix="/blogs/location", tags=["Locations"])


@router.get(
        "/blogs/location/{location_id}", 
        response_model=LocationResponseSchema)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(
        get_get_location_by_id_use_case),
) -> LocationResponseSchema:
    try:
        return await use_case.execute(location_id)
    except LocationNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


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
    try:
        return await use_case.execute(filter_location.location_id, new_data)
    except LocationNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.delete("/blogs/location", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    delete_filter: DeleteFilter,
    use_case: DeleteLocationUseCase = Depends(delete_location_use_case),
) -> None:
    if delete_filter.key != "pk":
        raise HTTPException(
            status_code=400, 
            detail="Можно удалять только по pk")
    try:
        await use_case.execute(delete_filter.value)
    except LocationNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )