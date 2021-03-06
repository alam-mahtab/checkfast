from typing import Optional
from pydantic import BaseModel, Field
import datetime

class CourseBase(BaseModel):
    title:str
    name :str
    desc:str
    price:int
    type:str
    status:int
    
class CourseList(CourseBase):
    created_date: Optional[datetime.datetime]

class CourseUpdate(BaseModel):
    #id : str = Field(..., example="Enter Your Id")
    title:str
    name :str
    desc:str
    type:str
    