from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> dict:
        """Удалить комментарий"""
        try:
            with self._database.session() as session:
                # Проверяем существование комментария
                comment = self._repo.get_by_id(session, comment_id)
                if not comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с ID {comment_id} не найден"
                    )

                # Удаляем комментарий
                deleted = self._repo.delete(session, comment_id)
                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить комментарий"
                    )

                return {"message": f"Комментарий с ID {comment_id} успешно удален"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении комментария: {e}")
            raise