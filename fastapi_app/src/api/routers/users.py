from fastapi import APIRouter, Depends, HTTPException, status

from api.depends import (
    create_user_use_case,
    get_get_user_by_login_use_case,
)

from core.exceptions.domain_exceptions import (
    UserLoginIsNotUniqueException,
    UserNotFoundByLoginException,
)

from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase

from schemas.users import User, CreateUser

router = APIRouter()


@router.get(
        "/user/{login}", 
        status_code=status.HTTP_200_OK, 
        response_model=User)
async def get_user_by_login(
    login: str,
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
) -> User:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: CreateUser,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> User:
    try:
        return await use_case.execute(user=user)
    except UserLoginIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
