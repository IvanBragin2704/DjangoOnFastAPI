import uuid
from fastapi import APIRouter


from src.domain.user.use_cases.classes import CreateUserUseCase, DeleteUserByUsernameUseCase, GetUserByUsernameUseCase, UpdateUserByUsernameUseCase
from src.domain.post.use_cases.classes import CreatePostUseCase, DeletePostUseCase, GetPostUseCase, UpdatePostUseCase
from src.domain.location.use_cases.classes import CreateLocationUseCase, DeleteLocationUseCase, GetLocationUseCase, UpdateLocationUseCase
from src.domain.comment.use_cases.classes import CreateCommentUseCase, DeleteCommentUseCase, GetCommentUseCase, UpdateCommentUseCase
from src.domain.category.use_cases.classes import CreateCategoryUseCase, UpdateCategoryUseCase, GetCategoryUseCase, DeleteCategoryUseCase


from src.schemas.user import UserResponseSchema, UserRequestSchema
from src.schemas.post import PostResponseSchema, PostRequestSchema
from src.schemas.location import LocationResponseSchema, LocationRequestSchema
from src.schemas.comment import CommentResponseSchema, CommentRequestSchema
from src.schemas.category import CategoryResponseSchema, CategoryRequestSchema

base_router = APIRouter()

# user
@base_router.get('/user/{username}', tags=['user'])
async def get_user_by_username(username: str) -> UserResponseSchema:
    use_case = GetUserByUsernameUseCase()
    return await use_case.execute(username=username)

@base_router.post('/user/', tags=['user'])
async def create_user(data: UserRequestSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    return await use_case.execute(data=data)

@base_router.delete('/user/{username}', tags=['user'])
async def delete_user_by_username(username: str):
    use_case = DeleteUserByUsernameUseCase()
    await use_case.execute(username)
    return {'message': f'Пользователь "{username}" успешно удален'}

# post
@base_router.get('/post/{id}', tags=['post'])
async def get_post(id: uuid.UUID) -> PostResponseSchema:
    use_case = GetPostUseCase()
    return await use_case.execute(id=id)

@base_router.post('/post/', tags=['post'])
async def create_post(data: PostRequestSchema) -> PostResponseSchema:
    use_case = CreatePostUseCase()
    return await use_case.execute(data=data)

@base_router.put('/post/{id}', tags=['post'])
async def update_post(id: uuid.UUID, data: PostRequestSchema) -> PostResponseSchema:
    use_case = UpdatePostUseCase()
    return await use_case.execute(id=id, data=data)

@base_router.delete('/post/{id}', tags=['post'])
async def delete_post(id: uuid.UUID):
    use_case = DeletePostUseCase()
    await use_case.execute(id)
    return {'message': f'Публикация с id "{id}" успешно удаленa'}

# location
@base_router.get('/location/{id}', tags=['location'])
async def get_location(id: uuid.UUID) -> LocationResponseSchema:
    use_case = GetLocationUseCase()
    return await use_case.execute(id=id)

@base_router.post('/location/', tags=['location'])
async def create_location(data: LocationRequestSchema) -> LocationResponseSchema:
    use_case = CreateLocationUseCase()
    return await use_case.execute(data=data)

@base_router.put('/location/{id}', tags=['location'])
async def update_location(
    id: uuid.UUID, data: LocationRequestSchema
) -> LocationResponseSchema:
    use_case = UpdateLocationUseCase()
    return await use_case.execute(id=id, data=data)

@base_router.delete('/location/{id}', tags=['location'])
async def delete_location(id: uuid.UUID):
    use_case = DeleteLocationUseCase()
    await use_case.execute(id)
    return {'message': f'Местоположение с id "{id}" успешно удалено'}

# comment
@base_router.get('/comment/{id}', tags=['comment'])
async def get_comment(id: uuid.UUID) -> CommentResponseSchema:
    use_case = GetCommentUseCase()
    return await use_case.execute(id=id)

@base_router.post('/comment/', tags=['comment'])
async def create_comment(data: CommentRequestSchema) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    return await use_case.execute(data=data)

@base_router.put('/comment/{id}', tags=['comment'])
async def update_comment(
    id: uuid.UUID, data: CommentRequestSchema
) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    return await use_case.execute(id=id, data=data)

@base_router.delete('/comment/{id}', tags=['comment'])
async def delete_comment(id: uuid.UUID):
    use_case = DeleteCommentUseCase()
    await use_case.execute(id)
    return {'message': f'Комментарий с id "{id}" успешно удален'}

# category
@base_router.get('/category/{id}', tags=['category'])
async def get_category(id: uuid.UUID) -> CategoryResponseSchema:
    use_case = GetCategoryUseCase()
    return await use_case.execute(id=id)

@base_router.post('/category/', tags=['category'])
async def create_category(data: CategoryRequestSchema) -> CategoryResponseSchema:
    use_case = CreateCategoryUseCase()
    return await use_case.execute(data=data)

@base_router.put('/category/{id}', tags=['category'])
async def update_category(
    id: uuid.UUID, data: CategoryRequestSchema
) -> CategoryResponseSchema:
    use_case = UpdateCategoryUseCase()
    return await use_case.execute(id=id, data=data)

@base_router.delete('/category/{id}', tags=['category'])
async def delete_category(id: uuid.UUID):
    use_case = DeleteCategoryUseCase()
    await use_case.execute(id)
    return {'message': f'Категория с id "{id}" успешно удаленa'}