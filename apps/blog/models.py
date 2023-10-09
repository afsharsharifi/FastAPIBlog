from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str
    is_published: bool = True
