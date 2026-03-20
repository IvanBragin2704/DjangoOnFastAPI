from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.posts import Post, PostUpdate


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UsersRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_id: int, post_data: PostUpdate) -> Post:
        """Обновить пост"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли пост
                existing_post = self._repo.get_by_id(session, post_id)
                if not existing_post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с ID {post_id} не найден"
                    )

                # Если меняется автор, проверяем его существование
                if post_data.author_id and post_data.author_id != existing_post.author_id:
                    author = self._user_repo.get_by_id(session, post_data.author_id)
                    if not author:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Автор с ID {post_data.author_id} не найден"
                        )

                # Если меняется категория, проверяем её существование
                if post_data.category_id and post_data.category_id != existing_post.category_id:
                    category = self._category_repo.get_by_id(session, post_data.category_id)
                    if not category:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Категория с ID {post_data.category_id} не найдена"
                        )

                # Если меняется локация, проверяем её существование
                if post_data.location_id and post_data.location_id != existing_post.location_id:
                    location = self._location_repo.get_by_id(session, post_data.location_id)
                    if not location:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Локация с ID {post_data.location_id} не найдена"
                        )

                # Обновляем пост
                updated_post = self._repo.update(session, post_id, post_data)
                return Post.model_validate(updated_post)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении поста: {e}")
            raise