from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, user_id: int) -> dict:
        """Удалить пользователя по ID"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли пользователь
                user = self._repo.get_by_id(session, user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с ID {user_id} не найден"
                    )

                # Удаляем пользователя
                deleted = self._repo.delete(session, user_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить пользователя"
                    )

                return {"message": f"Пользователь с ID {user_id} успешно удален"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {e}")
            raise