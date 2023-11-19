from datetime import datetime

from pydantic import BaseModel

from schemas.users import UserBase


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    owner_id: int
    owner: UserBase
    id: int
    created_at: datetime
