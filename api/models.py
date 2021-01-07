from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    Name: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int

class ImageSchema(BaseModel):
    name : str
    title : str
    description : str
    file: bytes

class ImageDB(ImageSchema):
    id : int