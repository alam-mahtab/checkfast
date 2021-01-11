from typing import Optional
from pydantic import BaseModel
import datetime

class SubjectBase(BaseModel):
    title:str
    name :str
    desc:str
    
class SubjectList(SubjectBase):
    created_date: Optional[datetime.datetime]