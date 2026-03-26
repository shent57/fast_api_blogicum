from typing import List

from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema


class GetLocationsUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(
        self, is_published: bool, name: str | None = None
    ) -> List[LocationResponseSchema]:
        with self._database.session() as session:
            locations = self._location_repository.get_all(
                session, 
                is_published)

            if is_published is not None:
                locations = [
                    loc for loc in locations 
                    if loc.is_published == is_published
                ]

            if name is not None:
                locations = [
                    loc 
                    for loc in locations 
                    if name.lower() in loc.name.lower()
                ]
            return [LocationResponseSchema
                    .model_validate(loc) for loc in locations]
