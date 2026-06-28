from pydantic import BaseModel


class PostCreate(BaseModel):
    username: str
    content: str
