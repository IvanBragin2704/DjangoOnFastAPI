from fastapi import APIRouter, Depends, status
from src.schemas.categories import Category, CategoryCreate, CategoryUpdate
from src.domain.categories.use_cases.get_category_by_id import GetCategoryByIdUseCase
from src.domain.categories.use_cases.create_category import CreateCategoryUseCase
from src.domain.categories.use_cases.update_category import UpdateCategoryUseCase
from src.domain.categories.use_cases.delete_category import DeleteCategoryUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends()
) -> Category:
    """Получить категорию по ID"""
    return await use_case.execute(category_id=category_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends()
) -> Category:
    """Создать новую категорию"""
    return await use_case.execute(category_data=category_data)


@router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    use_case: UpdateCategoryUseCase = Depends()
) -> Category:
    """Обновить категорию"""
    return await use_case.execute(category_id=category_id, category_data=category_data)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends()
) -> dict:
    """Удалить категорию по ID"""
    return await use_case.execute(category_id=category_id)