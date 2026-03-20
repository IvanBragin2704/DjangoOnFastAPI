from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment, CommentUpdate


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> Comment:
        """Обновить комментарий"""
        try:
            with self._database.session() as session:
                # Проверяем существование комментария
                existing_comment = self._repo.get_by_id(session, comment_id)
                if not existing_comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с ID {comment_id} не найден"
                    )

                # Обновляем комментарий
                updated_comment = self._repo.update(session, comment_id, comment_data)
                return Comment.model_validate(updated_comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении комментария: {e}")
            raise