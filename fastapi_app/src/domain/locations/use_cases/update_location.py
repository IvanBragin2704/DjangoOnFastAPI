from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.locations import Location, LocationUpdate


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> Location:
        """Обновить локацию"""
        try:
            with self._database.session() as session:
                # Проверяем, существует ли локация
                existing_location = self._repo.get_by_id(session, location_id)
                if not existing_location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                # Если меняется название, проверяем уникальность
                if location_data.name and location_data.name != existing_location.name:
                    same_name = session.query(self._repo.model).filter(
                        self._repo.model.name == location_data.name
                    ).first()
                    if same_name:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Локация с названием '{location_data.name}' уже существует"
                        )

                # Обновляем локацию
                updated_location = self._repo.update(session, location_id, location_data)
                return Location.model_validate(updated_location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении локации: {e}")
            raise