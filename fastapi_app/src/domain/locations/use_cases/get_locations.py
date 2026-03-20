from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.locations import Location


class GetLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, published_only: bool = False) -> list[Location]:
        try:
            with self._database.session() as session:
                if published_only:
                    locations = self._repo.get_published(session)
                else:
                    locations = self._repo.get_all(session)

                return [Location.model_validate(loc) for loc in locations]
        except Exception as e:
            print(f"Ошибка при получении локаций: {e}")
            raise