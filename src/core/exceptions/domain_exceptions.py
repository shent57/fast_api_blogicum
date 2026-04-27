class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail
        super().__init__(detail)

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)

        super().__init__(detail=detail)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с логином='{login}' уже существует")

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)

        super().__init__(detail=detail)


class PostPermissionException(BaseDomainException):
    _exception_text_template = "У вас нет прав для {action} поста"

    def __init__(self, action: str = "редактирования") -> None:
        detail = self._exception_text_template.format(action=action)

        super().__init__(detail=detail)


class CommentPermissionException(BaseDomainException):
    _exception_text_template = "У вас нет прав для {action} комментария"

    def __init__(self, action: str = "редактирования") -> None:
        detail = self._exception_text_template.format(action=action)

        super().__init__(detail=detail)


class PostNotFoundException(BaseDomainException):
    _exception_text_template = "Пост с id='{post_id}' не найден"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)

        super().__init__(detail=detail)


class CategoryNotFoundException(BaseDomainException):
    _exception_text_template = "Категория с id='{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)

        super().__init__(detail=detail)


class LocationNotFoundException(BaseDomainException):
    _exception_text_template = "Локация с id='{location_id}' не найдена"

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(location_id=location_id)

        super().__init__(detail=detail)


class WrongPasswordException(BaseDomainException):
    _exception_text = "Неверный пароль"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class UploadFileIsNotImageException(BaseDomainException):
    _exception_text = "Загружаемый файл не является JPEG изображением"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class PostHasNotImageException(BaseDomainException):
    _exception_text = "Данный пост не содержит изображения"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)
