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
