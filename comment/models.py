from pydantic import BaseModel, Field


class CommentSchema(BaseModel):
    Name: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class CommentDB(CommentSchema):
    id: int