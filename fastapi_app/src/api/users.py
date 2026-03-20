from fastapi import APIRouter, Depends, status
from src.schemas.users import User, UserCreate, UserUpdate
from src.domain.users.use_cases.get_users import GetUsersUseCase
from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from src.domain.users.use_cases.get_user_by_username import GetUserByUsernameUseCase
from src.domain.users.use_cases.create_user import CreateUserUseCase
from src.domain.users.use_cases.delete_user import DeleteUserUseCase
from src.domain.users.use_cases.update_user import UpdateUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_users(
    use_case: GetUsersUseCase = Depends()
) -> list[User]:
    return await use_case.execute()


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends()
) -> User:
    return await use_case.execute(user_id=user_id)


@router.get("/by-username/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends()
) -> User:
    return await use_case.execute(username=username)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> User:
    return await use_case.execute(user_data=user_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> dict:
    return await use_case.execute(user_id=user_id)


# НОВЫЙ PUT ЭНДПОИНТ
@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> User:
    """Обновить данные пользователя"""
    return await use_case.execute(user_id=user_id, user_data=user_data)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_users(
    use_case: GetUsersUseCase = Depends()
) -> list[User]:
    """Получить всех пользователей"""
    return await use_case.execute()


@router.get("/by-username/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends()
) -> User:
    """Получить пользователя по username"""
    return await use_case.execute(username=username)


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends()
) -> User:
    """Получить пользователя по ID"""
    return await use_case.execute(user_id=user_id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> User:
    """Создать нового пользователя"""
    return await use_case.execute(user_data=user_data)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> dict:
    """Удалить пользователя по ID"""
    return await use_case.execute(user_id=user_id)

@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> User:
    """Обновить данные пользователя"""
    return await use_case.execute(user_id=user_id, user_data=user_data)