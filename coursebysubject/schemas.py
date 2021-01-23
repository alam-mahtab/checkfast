from typing import Optional
from pydantic import BaseModel, Field
import datetime

class SubjectBase(BaseModel):
    title:str
    name :str
    desc:str
    
class SubjectList(SubjectBase):
    created_date: Optional[datetime.datetime]

class SubjectUpdate(BaseModel):
    #id : str = Field(..., example="Enter Your Id")
    title:str
    name :str
    desc:str
    