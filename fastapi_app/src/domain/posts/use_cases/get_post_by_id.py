from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.posts import Post


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> Post:
        """Получить пост по ID"""
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)

                if not post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с ID {post_id} не найден"
                    )

                return Post.model_validate(post)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении поста: {e}")
            raise