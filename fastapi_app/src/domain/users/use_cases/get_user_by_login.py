from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, login: str) -> User:
        """Получить пользователя по логину"""
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, login)

                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с логином '{login}' не найден"
                    )

                return User.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            raise