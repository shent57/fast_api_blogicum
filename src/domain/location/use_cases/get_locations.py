from typing import List
import logging
from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.infrastructure.sqlite.database import Database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.locations import LocationResponseSchema

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
        except LocationNotFoundException as e:  
            logger.error(e.get_detail())
            return []