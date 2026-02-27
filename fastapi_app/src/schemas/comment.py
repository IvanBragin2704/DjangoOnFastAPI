from pydantic import BaseModel, Field
from datetime import datetime

class Comment(BaseModel):
    text: str = Field(max_length=1000, description="Текст комментария")
    post_id: int = Field(description="ID поста")
    author_id: int = Field(description="ID автора")
    created_at: datetime = Field(default_factory=datetime.now, frozen=True)

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int
    author_id: int


class CommentUpdate(BaseModel):
    text: str | None = None