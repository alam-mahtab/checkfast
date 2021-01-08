from typing import Optional
from pydantic import BaseModel
import datetime

class PostBase(BaseModel):
    title:str
    name :str
    desc:str

class PostList(PostBase):
    created_date: Optional[datetime.datetime]
   