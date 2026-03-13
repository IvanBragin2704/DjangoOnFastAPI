import uuid
from fastapi import HTTPException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentRequestSchema, CommentResponseSchema



class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, data: CommentRequestSchema):
        with self._database.session() as session:
            comment = Comment(**data.model_dump())
            self._repo.create(session=session, comment=comment)

        return CommentResponseSchema.model_validate(obj=comment)

class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            comment = self._repo.get(session=session, id=id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id "{id}" не найден'
                )

        self._repo.delete(session=session, comment=comment)

class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: uuid.UUID) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, id=id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id "{id}" не найден'
                )

        return CommentResponseSchema.model_validate(obj=comment)

class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, id: uuid.UUID, data: CommentRequestSchema
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, id=id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id "{id}" не найден'
                )

            self._repo.update(session=session, comment=comment, data=data)

        return CommentResponseSchema.model_validate(obj=comment)

