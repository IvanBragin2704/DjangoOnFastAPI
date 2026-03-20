from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from src.infrastructure.sqlite.models.post import Post
from src.schemas.posts import PostCreate, PostUpdate


class PostRepository:
    def __init__(self):
        self.model = Post

    def get_by_id(self, session: Session, post_id: int) -> Optional[Post]:
        """Получить пост по ID (без связанных данных)"""
        return session.get(self.model, post_id)

    def create(self, session: Session, post_data: PostCreate) -> Post:
        """Создать новый пост"""
        from datetime import datetime
        post = self.model(
            title=post_data.title,
            text=post_data.text,
            pub_date=post_data.pub_date,
            author_id=post_data.author_id,
            category_id=post_data.category_id,
            location_id=post_data.location_id,
            image=post_data.image,
            is_published=post_data.is_published,
            created_at=datetime.now()
        )
        session.add(post)
        session.flush()
        return post

    def update(self, session: Session, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        """Обновить пост"""
        post = self.get_by_id(session, post_id)
        if not post:
            return None

        update_data = post_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(post, field):
                setattr(post, field, value)

        return post

    def delete(self, session: Session, post_id: int) -> bool:
        """Удалить пост"""
        post = self.get_by_id(session, post_id)
        if post:
            session.delete(post)
            return True
        return False