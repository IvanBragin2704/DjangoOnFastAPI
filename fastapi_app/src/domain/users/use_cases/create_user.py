from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User, UserCreate


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        try:
            with self._database.session() as session:
                # Проверяем, не занят ли username
                existing_username = self._repo.get_by_username(session, user_data.username)
                if existing_username:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Пользователь с username '{user_data.username}' уже существует"
                    )

                # Проверяем email, если он указан
                if user_data.email:
                    existing_email = session.query(self._repo.model).filter(
                        self._repo.model.email == user_data.email
                    ).first()
                    if existing_email:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с email '{user_data.email}' уже существует"
                        )

                # Создаем пользователя
                new_user = self._repo.create(session, user_data)

                return User.model_validate(new_user)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            raise