from typing import Optional

from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    content: str
    name: str
