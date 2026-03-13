from src.infrastructure.sqlite.models.user import User
from fastapi import HTTPException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserRequestSchema, UserResponseSchema


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserRequestSchema):
        with self._database.session() as session:
            user = User(
                **data.model_dump(exclude={'password'}),
                password=data.password.get_secret_value(),
            )
            self._repo.create(session=session, user=user)

        return UserResponseSchema.model_validate(obj=user)

class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserResponseSchema:
        with self._database.session() as session:
            user = self._repo.get(session=session, username=username)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь "{username}" не найден'
                )

        return UserResponseSchema.model_validate(obj=user)

class DeleteUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str):
        with self._database.session() as session:
            user = self._repo.get(session=session, username=username)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь "{username}" не найден'
                )

        self._repo.delete(session=session, user=user)

class UpdateUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, username: str, data: UserRequestSchema
    ) -> UserResponseSchema:
        with self._database.session() as session:
            user = self._repo.get(session=session, username=username)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь "{username}" не найден'
                )

            self._repo.update(session=session, user=user, data=data)

        return UserResponseSchema.model_validate(obj=user)
