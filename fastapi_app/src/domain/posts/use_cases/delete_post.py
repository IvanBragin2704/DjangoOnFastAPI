from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> dict:
        """Удалить пост по ID"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли пост
                post = self._repo.get_by_id(session, post_id)
                if not post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с ID {post_id} не найден"
                    )

                # Удаляем пост
                deleted = self._repo.delete(session, post_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить пост"
                    )

                return {"message": f"Пост с ID {post_id} успешно удален"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении поста: {e}")
            raise