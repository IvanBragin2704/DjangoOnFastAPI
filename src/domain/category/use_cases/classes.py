import uuid
from fastapi import HTTPException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.category import CategoryRequestSchema, CategoryResponseSchema


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryRequestSchema):
        with self._database.session() as session:
            category = Category(**data.model_dump())
            self._repo.create(session=session, category=category)

        return CategoryResponseSchema.model_validate(obj=category)

class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            category = self._repo.get(session=session, id=id)

            if category is None:
                raise HTTPException(
                    status_code=404, detail=f'Категория с id "{id}" не найдена'
                )

        self._repo.delete(session=session, category=category)

class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, id: uuid.UUID) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.get(session=session, id=id)

            if category is None:
                raise HTTPException(
                    status_code=404, detail=f'Категория с id "{id}" не найдена'
                )

        return CategoryResponseSchema.model_validate(obj=category)

class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, id: uuid.UUID, data: CategoryRequestSchema
    ) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.get(session=session, id=id)

            if category is None:
                raise HTTPException(
                    status_code=404, detail=f'Категория с id "{id}" не найдена'
                )

            self._repo.update(session=session, category=category, data=data)

        return CategoryResponseSchema.model_validate(obj=category)
