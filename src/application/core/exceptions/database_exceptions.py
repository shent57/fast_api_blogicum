class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        if self._detail:
            return self._detail
        return "Ошибка при работе с БД"


class EntityNotFoundException(BaseDatabaseException):
    pass


class EntityAlreadyExistsException(BaseDatabaseException):
    pass