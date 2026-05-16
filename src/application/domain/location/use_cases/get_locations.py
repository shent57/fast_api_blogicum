from typing import List
import logging
from src.application.core.exceptions.database_exceptions import EntityNotFoundException
from src.application.infrastructure.postgres.database import Database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from src.application.schemas.locations import LocationResponseSchema

logger = logging.getLogger(__name__)


class GetLocationsUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(
        self, is_published: bool, name: str | None = None
    ) -> List[LocationResponseSchema]:
        try:
            async with self._database.session() as session:
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
        except EntityNotFoundException as e:  
            logger.error(e.get_detail())
            return []