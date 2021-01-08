from typing import Optional
from pydantic import BaseModel, Field


class FeedSchema(BaseModel):
    Name: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    url = str


class FeedDB(FeedSchema):
    id: int
    

