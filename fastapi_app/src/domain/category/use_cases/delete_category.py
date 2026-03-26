from infrastructure.sqlite.database import Database
from infrastructure.sqlite.repositories.categories import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(
            self, 
            category_repository: CategoryRepository, 
            database: Database):
        self._category_repository = category_repository
        self._database = database

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            self._category_repository.delete(session, category_id)
