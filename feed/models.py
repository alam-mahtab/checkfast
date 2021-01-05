from pydantic import BaseModel, Field


class FeedSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class FeedDB(FeedSchema):
    id: int