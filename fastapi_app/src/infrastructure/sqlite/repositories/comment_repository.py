from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self):
        self.model = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Optional[Comment]:
        """Получить комментарий по ID"""
        return session.get(self.model, comment_id)

    def create(self, session: Session, comment_data: CommentCreate) -> Comment:
        """Создать новый комментарий"""
        from datetime import datetime

        comment = self.model(
            text=comment_data.text,
            post_id=comment_data.post_id,
            author_id=comment_data.author_id,
            created_at=datetime.now()
        )
        session.add(comment)
        session.flush()
        return comment

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        """Обновить комментарий (только текст)"""
        comment = self.get_by_id(session, comment_id)
        if not comment:
            return None

        comment.text = comment_data.text
        return comment

    def delete(self, session: Session, comment_id: int) -> bool:
        """Удалить комментарий"""
        comment = self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            return True
        return False