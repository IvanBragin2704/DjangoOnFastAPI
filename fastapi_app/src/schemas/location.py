from pydantic import BaseModel, Field, ConfigDict

class LocationBase(BaseModel):
    name: str = Field(max_length=256 , description="Название локации")
    is_published: bool = Field(True, description="Опубликовано")


class Location(LocationBase):
    """Полная модель локаций"""
    id:int
    model_config = ConfigDict(from_attributes=True)