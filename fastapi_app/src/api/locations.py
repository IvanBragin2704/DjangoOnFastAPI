from fastapi import APIRouter, Depends, Query, status
from src.schemas.locations import Location, LocationCreate, LocationUpdate
from src.domain.locations.use_cases.get_locations import GetLocationsUseCase
from src.domain.locations.use_cases.create_location import CreateLocationUseCase
from src.domain.locations.use_cases.update_location import UpdateLocationUseCase
from src.domain.locations.use_cases.delete_location import DeleteLocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[Location], status_code=status.HTTP_200_OK)
async def get_locations(
    published_only: bool = Query(False, description="Только опубликованные"),
    use_case: GetLocationsUseCase = Depends()
) -> list[Location]:
    """Получить все локации"""
    return await use_case.execute(published_only=published_only)


@router.get("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationsUseCase = Depends()  # или создать отдельный use case
) -> Location:
    """Получить локацию по ID"""
    locations = await use_case.execute()
    for location in locations:
        if location.id == location_id:
            return location
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Локация с ID {location_id} не найдена"
    )


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    use_case: CreateLocationUseCase = Depends()
) -> Location:
    """Создать новую локацию"""
    return await use_case.execute(location_data=location_data)


@router.put("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_case: UpdateLocationUseCase = Depends()
) -> Location:
    """Обновить локацию"""
    return await use_case.execute(location_id=location_id, location_data=location_data)


@router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(
    location_id: int,
    use_case: DeleteLocationUseCase = Depends()
) -> dict:
    """Удалить локацию"""
    return await use_case.execute(location_id=location_id)