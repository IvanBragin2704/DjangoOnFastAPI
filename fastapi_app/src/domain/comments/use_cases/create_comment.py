from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.comments import Comment, CommentCreate


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UsersRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        """Создать новый комментарий"""
        try:
            with self._database.session() as session:
                # Проверяем существование автора
                author = self._user_repo.get_by_id(session, comment_data.author_id)
                if not author:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Автор с ID {comment_data.author_id} не найден"
                    )

                # Проверяем существование поста
                post = self._post_repo.get_by_id(session, comment_data.post_id)
                if not post:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Пост с ID {comment_data.post_id} не найден"
                    )

                # Создаем комментарий
                new_comment = self._repo.create(session, comment_data)
                return Comment.model_validate(new_comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании комментария: {e}")
            raise