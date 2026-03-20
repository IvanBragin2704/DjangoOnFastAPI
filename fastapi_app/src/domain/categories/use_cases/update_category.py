from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.categories import Category, CategoryUpdate


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> Category:
        """Обновить категорию"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли категория
                existing_category = self._repo.get_by_id(session, category_id)
                if not existing_category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                # Если обновляется slug, проверяем уникальность
                if category_data.slug and category_data.slug != existing_category.slug:
                    same_slug = self._repo.get_by_slug(session, category_data.slug)
                    if same_slug:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Категория со slug '{category_data.slug}' уже существует"
                        )

                # Обновляем категорию
                updated_category = self._repo.update(session, category_id, category_data)

                if not updated_category:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось обновить категорию"
                    )

                return Category.model_validate(updated_category)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении категории: {e}")
            raise