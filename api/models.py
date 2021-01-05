from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int

class ImageSchema(BaseModel):
    name : str
    title : str
    description : str
    url : bytes
    

class ImageDB(ImageSchema):
    id : int