from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get_by_id(self, session: Session, category_id: int) -> Optional[Category]:
        """Получить категорию по ID"""
        return session.get(self.model, category_id)

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        return session.query(self.model).filter(self.model.slug == slug).first()

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
        """Создать новую категорию"""
        from datetime import datetime

        category = self.model(
            title=category_data.title,
            description=category_data.description,
            slug=category_data.slug,
            is_published=category_data.is_published,
            created_at=datetime.now()  # дата создания автоматически
        )
        session.add(category)
        session.flush()
        return category

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """Обновить категорию"""
        category = self.get_by_id(session, category_id)
        if not category:
            return None

        # Обновляем только переданные поля
        update_data = category_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(category, field):
                setattr(category, field, value)

        return category

    def delete(self, session: Session, category_id: int) -> bool:
        """Удалить категорию по ID"""
        category = self.get_by_id(session, category_id)
        if category:
            session.delete(category)
            return True
        return False