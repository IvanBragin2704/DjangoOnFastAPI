from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.posts import Post, PostCreate


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UsersRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_data: PostCreate) -> Post:
        """Создать новый пост"""
        try:
            with self._database.session() as session:
                # Проверяем существование автора
                author = self._user_repo.get_by_id(session, post_data.author_id)
                if not author:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Автор с ID {post_data.author_id} не найден"
                    )

                # Проверяем существование категории (если указана)
                if post_data.category_id:
                    category = self._category_repo.get_by_id(session, post_data.category_id)
                    if not category:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Категория с ID {post_data.category_id} не найдена"
                        )

                # Проверяем существование локации (если указана)
                if post_data.location_id:
                    location = self._location_repo.get_by_id(session, post_data.location_id)
                    if not location:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Локация с ID {post_data.location_id} не найдена"
                        )

                # Создаем пост
                new_post = self._repo.create(session, post_data)
                return Post.model_validate(new_post)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании поста: {e}")
            raise