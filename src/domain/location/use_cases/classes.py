import uuid
from fastapi import HTTPException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.location import LocationRequestSchema, LocationResponseSchema


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationRequestSchema):
        with self._database.session() as session:
            location = Location(**data.model_dump())
            self._repo.create(session=session, location=location)

        return LocationResponseSchema.model_validate(obj=location)

class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            location = self._repo.get(session=session, id=id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id "{id}" не найдено'
                )

        self._repo.delete(session=session, location=location)

class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, id: uuid.UUID) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._repo.get(session=session, id=id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id "{id}" не найдено'
                )

        return LocationResponseSchema.model_validate(obj=location)

class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, id: uuid.UUID, data: LocationRequestSchema
    ) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._repo.get(session=session, id=id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id "{id}" не найдено'
                )

            self._repo.update(session=session, location=location, data=data)

        return LocationResponseSchema.model_validate(obj=location)