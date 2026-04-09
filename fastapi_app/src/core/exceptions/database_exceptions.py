class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        if self._detail:
            return self._detail
        return "Ошибка при работе с БД"


class UserNotFoundException(BaseDatabaseException):
    def __init__(self, user_id: int | None = None, username: str | None = None):
        if user_id:
            detail = f"Пользователь с id={user_id} не найден"
        elif username:
            detail = f"Пользователь с username={username} не найден"
        else:
            detail = "Пользователь не найден"

        super().__init__(detail=detail)

class UserAlreadyExistsException(BaseDatabaseException):
    def __init__(self, user_id: int | None = None, username: str | None = None):
        if user_id:
            detail = f"Пользователь с id={user_id} уже существует"
        elif username:
            detail = f"Пользователь с username='{username}' уже существует"
        else:
            detail = "Пользователь уже существует"

        super().__init__(detail=detail)


class PostNotFoundException(BaseDatabaseException):
    def __init__(self, post_id: int | None = None):
        if post_id:
            detail = f"Пост с id='{post_id}' не найден"
        else:
            detail = "Пост не найден"

        super().__init__(detail=detail)


class PostAlreadyExistsException(BaseDatabaseException):
    def __init__(self, title: str | None = None):
        if title:
            detail = f"Пост с заголовком {title} уже существует"
        else:
            detail = "Пост с таким заголовком уже существует"

        super().__init__(detail=detail)


class CommentNotFoundException(BaseDatabaseException):
    def __init__(self, comment_id: int | None = None):
        if comment_id:
            detail = f"Комментарий с id='{comment_id}' не найден"
        else:
            detail = "Комментарий не найден"

        super().__init__(detail=detail)


class CommentAlreadyExistsException(BaseDatabaseException):
    def __init__(self, comment_id: int | None = None):
        if comment_id:
            detail = f"Комментарий с id={comment_id} уже существует"
        else:
            detail = "Комментарий уже существует"

        super().__init__(detail=detail)


class LocationNotFoundException(BaseDatabaseException):
    def __init__(self, location_id: int | None = None):
        if location_id:
            detail = f"Локация с id='{location_id}' не найдена"
        else:
            detail = "Локация не найдена"

        super().__init__(detail=detail)


class LocationAlreadyExistsException(BaseDatabaseException):
    def __init__(self, name: str | None = None):
        if name:
            detail = f"Локация с названием '{name}' уже существует"
        else:
            detail = "Локация с таким названием уже существует"

        super().__init__(detail=detail)


class CategoryNotFoundException(BaseDatabaseException):
    def __init__(self, category_id: int | None = None, slug: str | None = None):
        if category_id:
            detail = f"Категория с id='{category_id}' не найдена"
        elif slug:
            detail = f"Категория с slug='{slug}' не найдена"
        else:
            detail = "Категория не найдена"

        super().__init__(detail=detail)


class CategoryAlreadyExistsException(BaseDatabaseException):
    def __init__(self, slug: str | None = None):
        if slug:
            detail = f"Категория с названием '{slug}' уже существует"
        else:
            detail = "Категория с таким названием уже существует"

        super().__init__(detail=detail)