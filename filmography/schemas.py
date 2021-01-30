from typing import Optional
from pydantic import BaseModel
import datetime
class TutorBase(BaseModel):
    title:str
    desc:str
    status:int
    
class TutorList(TutorBase):
    created_date: Optional[datetime.datetime]