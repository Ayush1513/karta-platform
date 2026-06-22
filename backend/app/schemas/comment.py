from pydantic import BaseModel


class CommentCreate(BaseModel):

    comment: str