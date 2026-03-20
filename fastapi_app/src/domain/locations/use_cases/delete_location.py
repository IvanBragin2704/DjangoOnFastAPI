from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> dict:
        """Удалить локацию"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли локация
                location = self._repo.get_by_id(session, location_id)
                if not location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                # Удаляем локацию
                deleted = self._repo.delete(session, location_id)
                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить локацию"
                    )

                return {"message": f"Локация с ID {location_id} успешно удалена"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении локации: {e}")
            raise