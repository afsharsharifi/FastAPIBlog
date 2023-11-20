from pydantic import BaseModel


class Vote(BaseModel):
    post_id: int
