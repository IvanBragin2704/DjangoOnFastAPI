from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        """Удалить категорию по ID"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли категория
                category = self._repo.get_by_id(session, category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                # Удаляем категорию
                deleted = self._repo.delete(session, category_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить категорию"
                    )

                return {"message": f"Категория с ID {category_id} успешно удалена"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении категории: {e}")
            raise