from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationCreate, LocationUpdate


class LocationRepository:
    def __init__(self):
        self.model = Location

    def get_by_id(self, session: Session, location_id: int) -> Optional[Location]:
        """Получить локацию по ID"""
        return session.get(self.model, location_id)

    def get_all(self, session: Session) -> List[Location]:
        """Получить все локации"""
        return session.query(self.model).all()

    def get_published(self, session: Session) -> List[Location]:
        """Получить только опубликованные локации"""
        return session.query(self.model).filter(self.model.is_published.is_(True)).all()

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        """Создать новую локацию"""
        from datetime import datetime

        location = self.model(
            name=location_data.name,
            is_published=location_data.is_published,
            created_at=datetime.now()
        )
        session.add(location)
        session.flush()
        return location

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Optional[Location]:
        """Обновить локацию"""
        location = self.get_by_id(session, location_id)
        if not location:
            return None

        update_data = location_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(location, field):
                setattr(location, field, value)

        return location

    def delete(self, session: Session, location_id: int) -> bool:
        """Удалить локацию"""
        location = self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            return True
        return False