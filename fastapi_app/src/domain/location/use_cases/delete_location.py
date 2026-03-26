from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.locations import LocationRepository


class DeleteLocationUseCase:
    def __init__(self, 
                 location_repository: LocationRepository, 
                 database: Database):
        self._location_repository = location_repository
        self._database = database

    async def execute(self, location_id: int) -> None:
        with self._database.session() as session:
            self._location_repository.delete(session, location_id)
