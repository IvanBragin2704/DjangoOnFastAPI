from fastapi import APIRouter, Depends, status
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.domain.comments.use_cases.get_comment_by_id import GetCommentByIdUseCase
from src.domain.comments.use_cases.create_comment import CreateCommentUseCase
from src.domain.comments.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comments.use_cases.delete_comment import DeleteCommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])




@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends()
) -> Comment:
    """Получить комментарий по ID"""
    return await use_case.execute(comment_id=comment_id)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    use_case: CreateCommentUseCase = Depends()
) -> Comment:
    """Создать новый комментарий"""
    return await use_case.execute(comment_data=comment_data)


@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends()
) -> Comment:
    """Обновить комментарий"""
    return await use_case.execute(comment_id=comment_id, comment_data=comment_data)


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends()
) -> dict:
    """Удалить комментарий"""
    return await use_case.execute(comment_id=comment_id)