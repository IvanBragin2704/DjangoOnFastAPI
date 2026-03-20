from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, username: str) -> User:
        """Получить пользователя по username"""
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)

                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с username '{username}' не найден"
                    )

                return User.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            raise