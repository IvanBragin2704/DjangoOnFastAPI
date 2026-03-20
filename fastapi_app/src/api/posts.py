from fastapi import APIRouter, Depends, status
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.domain.posts.use_cases.get_post_by_id import GetPostByIdUseCase
from src.domain.posts.use_cases.create_post import CreatePostUseCase
from src.domain.posts.use_cases.update_post import UpdatePostUseCase
from src.domain.posts.use_cases.delete_post import DeletePostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends()
) -> Post:
    """Получить пост по ID"""
    return await use_case.execute(post_id=post_id)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePostUseCase = Depends()
) -> Post:
    """Создать новый пост"""
    return await use_case.execute(post_data=post_data)


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    use_case: UpdatePostUseCase = Depends()
) -> Post:
    """Обновить пост"""
    return await use_case.execute(post_id=post_id, post_data=post_data)


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    use_case: DeletePostUseCase = Depends()
) -> dict:
    """Удалить пост по ID"""
    return await use_case.execute(post_id=post_id)