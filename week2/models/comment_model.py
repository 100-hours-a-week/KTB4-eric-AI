from typing import Optional

from sqlmodel import SQLModel, Field


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    post_id: int = Field(foreign_key="post.id")
    content: str
    name: str